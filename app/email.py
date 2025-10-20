import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import httpx
import logging
import asyncio

logger = logging.getLogger(__name__)

USE_ETHEREAL = False  # Set to True to use real Ethereal, False to just log

async def create_ethereal_account():
    """
    Create a temporary Ethereal email account for testing.
    Returns SMTP credentials and account info.
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                'https://api.nodemailer.com/user',
                headers={'Content-Type': 'application/json'},
                json={
                    "requestor": "blkxchange",
                    "version": "1.0.0"
                }
            )
            if response.status_code in [200, 201]:
                return response.json()
            else:
                logger.error(f"Failed to create Ethereal account: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return None
    except Exception as e:
        logger.error(f"Error creating Ethereal account: {e}")
        return None

async def log_email_to_console(to_email: str, vendor_name: str, vendor_id: str):
    """
    Log email content to console instead of sending (for MVP testing).
    """
    setup_link = f"https://blkxchangemarketplace-kytxrr7p.devinapps.com/vendor/dashboard?id={vendor_id}"
    
    print("\n" + "="*80)
    print("📧 VENDOR WELCOME EMAIL (Console Mode)")
    print("="*80)
    print(f"To: {to_email}")
    print(f"From: BlkXchange™ <noreply@blkxchange.com>")
    print(f"Subject: Welcome to BlkXchange™ - The Internet's Black Wall Street")
    print("\n" + "-"*80)
    print(f"Welcome, {vendor_name}!")
    print("")
    print("We're thrilled to have you join BlkXchange™, a platform dedicated to")
    print("empowering Black and BIPOC entrepreneurs.")
    print("")
    print("Your vendor application has been received and is being reviewed by our team.")
    print("We'll notify you within 2-3 business days about your approval status.")
    print("")
    print("What You Get as a BlkXchange™ Vendor:")
    print("  • No Upfront Fees: Only pay when you make a sale (10% platform fee)")
    print("  • 90% Revenue Share: You keep 90% of every sale")
    print("  • Community Impact: 3% of sales support HBCUs and scholarships")
    print("  • Targeted Audience: Reach customers seeking Black-owned businesses")
    print("  • Full Dashboard: Manage products, orders, and track your impact")
    print("")
    print(f"View your application status: {setup_link}")
    print("")
    print("Together, we rise.")
    print("")
    print("BlkXchange™ - Empower. Exchange. Elevate.")
    print("="*80 + "\n")
    
    return {
        "success": True,
        "mode": "console_log",
        "message": "Email logged to console (MVP mode)"
    }

async def send_vendor_welcome_email(to_email: str, vendor_name: str, vendor_id: str):
    """
    Send a welcome email to a new vendor using Ethereal Email for testing.
    Returns the preview URL where the email can be viewed.
    """
    try:
        if not USE_ETHEREAL:
            return await log_email_to_console(to_email, vendor_name, vendor_id)
        account = await create_ethereal_account()
        
        if not account:
            logger.error("Could not create Ethereal account")
            return None
        
        smtp_host = account['smtp']['host']
        smtp_port = account['smtp']['port']
        smtp_secure = account['smtp']['secure']
        smtp_user = account['user']
        smtp_pass = account['pass']
        
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Welcome to BlkXchange™ - The Internet\'s Black Wall Street'
        message['From'] = 'BlkXchange™ <noreply@blkxchange.com>'
        message['To'] = to_email
        
        setup_link = f"https://blkxchangemarketplace-kytxrr7p.devinapps.com/vendor/dashboard?id={vendor_id}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Inter', Arial, sans-serif;
                    background-color: #F8F8F6;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background-color: #FFFFFF;
                    border: 2px solid #C5A14E;
                    border-radius: 8px;
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #000000 0%, #1A1A1A 100%);
                    color: #C5A14E;
                    padding: 40px 20px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-family: 'Playfair Display', serif;
                    font-size: 32px;
                    font-weight: bold;
                }}
                .content {{
                    padding: 40px 30px;
                    color: #1A1A1A;
                }}
                .content h2 {{
                    color: #000000;
                    font-size: 24px;
                    margin-top: 0;
                }}
                .content p {{
                    line-height: 1.6;
                    font-size: 16px;
                    color: #333333;
                }}
                .cta-button {{
                    display: inline-block;
                    background-color: #C5A14E;
                    color: #000000;
                    padding: 15px 40px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 16px;
                    margin: 20px 0;
                }}
                .cta-button:hover {{
                    background-color: #B39145;
                }}
                .benefits {{
                    background-color: #F8F8F6;
                    padding: 20px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .benefits ul {{
                    margin: 10px 0;
                    padding-left: 20px;
                }}
                .benefits li {{
                    margin: 10px 0;
                    color: #333333;
                }}
                .footer {{
                    background-color: #1A1A1A;
                    color: #C5A14E;
                    padding: 30px 20px;
                    text-align: center;
                    font-size: 14px;
                }}
                .footer p {{
                    margin: 5px 0;
                    color: #999999;
                }}
                .tagline {{
                    color: #C5A14E;
                    font-style: italic;
                    margin-top: 15px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>BlkXchange™</h1>
                    <p style="margin: 10px 0 0 0; color: #F8F8F6;">The Internet's Black Wall Street</p>
                </div>
                
                <div class="content">
                    <h2>Welcome, {vendor_name}! 🎉</h2>
                    
                    <p>We're thrilled to have you join BlkXchange™, a platform dedicated to empowering Black and BIPOC entrepreneurs.</p>
                    
                    <p>Your vendor application has been received and is being reviewed by our team. We'll notify you within 2-3 business days about your approval status.</p>
                    
                    <div class="benefits">
                        <h3 style="margin-top: 0; color: #000000;">What You Get as a BlkXchange™ Vendor:</h3>
                        <ul>
                            <li><strong>No Upfront Fees:</strong> Only pay when you make a sale (10% platform fee)</li>
                            <li><strong>90% Revenue Share:</strong> You keep 90% of every sale</li>
                            <li><strong>Community Impact:</strong> 3% of sales support HBCUs and scholarships</li>
                            <li><strong>Targeted Audience:</strong> Reach customers seeking Black-owned businesses</li>
                            <li><strong>Full Dashboard:</strong> Manage products, orders, and track your impact</li>
                        </ul>
                    </div>
                    
                    <p>Once approved, you'll receive another email with instructions to complete your vendor setup and start listing products.</p>
                    
                    <div style="text-align: center;">
                        <a href="{setup_link}" class="cta-button">View Your Application Status</a>
                    </div>
                    
                    <p>If you have any questions, feel free to reply to this email or visit our Help Center.</p>
                    
                    <p>Thank you for being part of the movement to build a sustainable digital economy that reinvests in our community.</p>
                    
                    <p><strong>Together, we rise.</strong></p>
                </div>
                
                <div class="footer">
                    <p><strong>BlkXchange™</strong></p>
                    <p class="tagline">Empower. Exchange. Elevate.</p>
                    <p style="margin-top: 20px;">© 2025 BlkXchange™. All rights reserved.</p>
                    <p>This is an automated message. Please do not reply directly to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Welcome to BlkXchange™ - The Internet's Black Wall Street
        
        Welcome, {vendor_name}!
        
        We're thrilled to have you join BlkXchange™, a platform dedicated to empowering Black and BIPOC entrepreneurs.
        
        Your vendor application has been received and is being reviewed by our team. We'll notify you within 2-3 business days about your approval status.
        
        What You Get as a BlkXchange™ Vendor:
        - No Upfront Fees: Only pay when you make a sale (10% platform fee)
        - 90% Revenue Share: You keep 90% of every sale
        - Community Impact: 3% of sales support HBCUs and scholarships
        - Targeted Audience: Reach customers seeking Black-owned businesses
        - Full Dashboard: Manage products, orders, and track your impact
        
        Once approved, you'll receive another email with instructions to complete your vendor setup and start listing products.
        
        View your application status: {setup_link}
        
        If you have any questions, feel free to reply to this email or visit our Help Center.
        
        Thank you for being part of the movement to build a sustainable digital economy that reinvests in our community.
        
        Together, we rise.
        
        ---
        BlkXchange™
        Empower. Exchange. Elevate.
        © 2025 BlkXchange™. All rights reserved.
        """
        
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        
        message.attach(part1)
        message.attach(part2)
        
        await aiosmtplib.send(
            message,
            hostname=smtp_host,
            port=smtp_port,
            username=smtp_user,
            password=smtp_pass,
            use_tls=smtp_secure
        )
        
        preview_url = f"https://ethereal.email/message/{message['Message-ID']}" if 'Message-ID' in message else None
        
        logger.info(f"✅ Vendor welcome email sent successfully to {to_email}")
        logger.info(f"📧 Preview URL: {preview_url or 'Check Ethereal inbox at https://ethereal.email'}")
        logger.info(f"📧 Ethereal Login - User: {smtp_user}, Pass: {smtp_pass}")
        logger.info(f"📧 View inbox at: https://ethereal.email/login")
        
        return {
            "success": True,
            "preview_url": preview_url,
            "ethereal_user": smtp_user,
            "ethereal_pass": smtp_pass,
            "ethereal_inbox": "https://ethereal.email/login"
        }
        
    except Exception as e:
        logger.error(f"❌ Error sending vendor welcome email: {e}")
        return {
            "success": False,
            "error": str(e)
        }
