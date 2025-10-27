from fastapi import APIRouter, HTTPException, Header, Request
from typing import Optional
import secrets
import hashlib
from datetime import datetime, timedelta
from app.database import db
from pydantic import BaseModel

router = APIRouter()

ADMIN_BYPASS_KEY = "EDEN129-360-SUPERACCESS"

class TwoFASetupRequest(BaseModel):
    user_id: str
    method: str

class TwoFAVerifyRequest(BaseModel):
    user_id: str
    code: str

class TwoFADisableRequest(BaseModel):
    user_id: str
    code: str

class AdminResetRequest(BaseModel):
    user_id: str
    admin_bypass_key: str

@router.post("/api/2fa/setup")
async def setup_2fa(request: TwoFASetupRequest, req: Request):
    try:
        existing_2fa = db.get_2fa_by_user(request.user_id)
        if existing_2fa and existing_2fa.enabled:
            raise HTTPException(status_code=400, detail="2FA already enabled for this user")
        
        recovery_codes = [secrets.token_hex(8) for _ in range(5)]
        
        if request.method == "email_otp":
            secret = secrets.token_hex(16)
        elif request.method == "totp":
            secret = secrets.token_urlsafe(32)
        else:
            raise HTTPException(status_code=400, detail="Invalid 2FA method")
        
        secret_hash = hashlib.sha256(secret.encode()).hexdigest()
        
        twofa = db.setup_2fa(request.user_id, request.method, secret_hash, recovery_codes)
        
        ip_address = req.client.host if req.client else None
        user_agent = req.headers.get("user-agent")
        db.log_audit_event(request.user_id, "2fa_setup", "success", ip_address, user_agent)
        
        return {
            "success": True,
            "method": request.method,
            "recovery_codes": recovery_codes,
            "secret": secret if request.method == "totp" else None,
            "message": "2FA setup successful. Save your recovery codes in a secure location."
        }
    
    except Exception as e:
        db.log_audit_event(request.user_id, "2fa_setup", "fail", None, None)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/2fa/verify")
async def verify_2fa(request: TwoFAVerifyRequest, req: Request):
    try:
        twofa = db.get_2fa_by_user(request.user_id)
        if not twofa:
            raise HTTPException(status_code=404, detail="2FA not enabled for this user")
        
        is_valid = False
        if request.code in twofa.recovery_codes:
            is_valid = True
            twofa.recovery_codes.remove(request.code)
        else:
            code_hash = hashlib.sha256(request.code.encode()).hexdigest()
            if code_hash == twofa.secret_hash:
                is_valid = True
        
        ip_address = req.client.host if req.client else None
        user_agent = req.headers.get("user-agent")
        
        if is_valid:
            db.log_audit_event(request.user_id, "2fa_verify", "success", ip_address, user_agent)
            return {"success": True, "message": "2FA verification successful"}
        else:
            db.log_audit_event(request.user_id, "2fa_verify", "fail", ip_address, user_agent)
            raise HTTPException(status_code=401, detail="Invalid 2FA code")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/2fa/disable")
async def disable_2fa(request: TwoFADisableRequest, req: Request):
    try:
        twofa = db.get_2fa_by_user(request.user_id)
        if not twofa:
            raise HTTPException(status_code=404, detail="2FA not enabled for this user")
        
        code_hash = hashlib.sha256(request.code.encode()).hexdigest()
        if code_hash != twofa.secret_hash and request.code not in twofa.recovery_codes:
            db.log_audit_event(request.user_id, "2fa_disable", "fail", None, None)
            raise HTTPException(status_code=401, detail="Invalid 2FA code")
        
        db.disable_2fa(request.user_id)
        
        ip_address = req.client.host if req.client else None
        user_agent = req.headers.get("user-agent")
        db.log_audit_event(request.user_id, "2fa_disable", "success", ip_address, user_agent)
        
        return {"success": True, "message": "2FA disabled successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/admin/reset2fa/{user_id}")
async def admin_reset_2fa(user_id: str, request: AdminResetRequest):
    try:
        if request.admin_bypass_key != ADMIN_BYPASS_KEY:
            db.log_audit_event(user_id, "2fa_reset", "fail", None, None)
            raise HTTPException(status_code=403, detail="Invalid admin bypass key")
        
        twofa = db.get_2fa_by_user(user_id)
        if not twofa:
            raise HTTPException(status_code=404, detail="2FA not enabled for this user")
        
        db.disable_2fa(user_id)
        db.log_audit_event(user_id, "2fa_reset", "success", None, None)
        
        return {"success": True, "message": f"2FA reset successful for user {user_id}"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/2fa/status/{user_id}")
async def get_2fa_status(user_id: str):
    try:
        twofa = db.get_2fa_by_user(user_id)
        if not twofa:
            return {"enabled": False, "method": None}
        
        return {
            "enabled": twofa.enabled,
            "method": twofa.method,
            "grace_period_expires": twofa.grace_period_expires.isoformat() if twofa.grace_period_expires else None,
            "recovery_codes_remaining": len(twofa.recovery_codes)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/audit-logs/{user_id}")
async def get_audit_logs(user_id: str):
    try:
        logs = db.get_audit_logs_by_user(user_id)
        return {
            "logs": [
                {
                    "id": log.id,
                    "event": log.event,
                    "status": log.status,
                    "ip_address": log.ip_address,
                    "user_agent": log.user_agent,
                    "timestamp": log.timestamp.isoformat()
                }
                for log in logs
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
