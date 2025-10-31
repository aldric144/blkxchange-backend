# BlkXchange™ Email Integration

## Overview

The BlkXchange™ backend now includes email notification functionality for vendor registration. The system is configured to use **Console Logging Mode** for MVP testing, with the option to enable **Ethereal Email** for browser-based email preview.

## Implementation Details

### Email Module (`app/email.py`)

The email module provides two modes of operation:

1. **Console Logging Mode (Default)**: Logs email content directly to the console/terminal for easy testing during development
2. **Ethereal Email Mode**: Creates temporary test email accounts and sends emails via Ethereal's SMTP service

### Configuration

To switch between modes, edit `/home/ubuntu/blkxchange/blkxchange-backend/app/email.py`:

```python
USE_ETHEREAL = False  # Set to True to enable Ethereal Email, False for console logging
```

### Vendor Registration Email

When a new vendor registers, the system automatically sends a welcome email with:

- **Subject**: "Welcome to BlkXchange™ - The Internet's Black Wall Street"
- **From**: BlkXchange™ <noreply@blkxchange.com>
- **Content**:
  - Welcome message
  - Application status information
  - Benefits of being a BlkXchange™ vendor:
    - No upfront fees (10% platform fee on sales)
    - 90% revenue share
    - 3% of sales support HBCUs and scholarships
    - Targeted audience
    - Full vendor dashboard
  - Link to vendor dashboard
  - Brand tagline: "Empower. Exchange. Elevate."

### Console Output Example

When a vendor registers, you'll see output like this in the backend logs:

```
================================================================================
📧 VENDOR WELCOME EMAIL SENT!
================================================================================
✅ Email sent to: vendor@example.com
👤 Vendor: John Doe (Doe's Business)
🔑 Vendor ID: abc123-def456-ghi789

📋 MODE: Console Logging (MVP)
   Email content has been logged above.
   To enable real Ethereal emails, set USE_ETHEREAL=True in app/email.py
================================================================================
```

## Testing

### Local Testing

1. Start the backend:
   ```bash
   cd /home/ubuntu/blkxchange/blkxchange-backend
   poetry run fastapi dev app/main.py
   ```

2. Register a vendor:
   ```bash
   curl -X POST http://localhost:8000/api/vendors \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test@example.com",
       "name": "Test Vendor",
       "business_name": "Test Business",
       "business_description": "Testing email",
       "phone": "555-1234"
     }'
   ```

3. Check the terminal output for the email notification

### Deployed Testing

The email functionality is live on the deployed backend at: https://app-tcqwzext.fly.dev

Test by submitting the vendor registration form on the frontend: https://blkxchangemarketplace-kytxrr7p.devinapps.com/vendor-register

Check the Fly.io logs to see the email output:
```bash
cd /home/ubuntu/blkxchange/blkxchange-backend
# Use the deploy tool to view logs
```

## Ethereal Email Integration (Optional)

To enable Ethereal Email for browser-based email preview:

1. Set `USE_ETHEREAL = True` in `app/email.py`
2. Redeploy the backend
3. When a vendor registers, the console will show:
   - Ethereal login URL
   - Temporary username and password
   - Direct preview URL (if available)
4. Visit the Ethereal inbox to view the rendered HTML email

### Ethereal Email Features

- **No signup required**: Accounts are created automatically for each email
- **Free service**: No payment or configuration needed
- **Browser preview**: View emails in a web browser with full HTML rendering
- **Temporary inboxes**: Each test creates a new temporary inbox

## Dependencies

The email integration uses the following Python packages:

- `aiosmtplib` (v5.0.0): Async SMTP client for Python
- `httpx`: HTTP client for Ethereal API calls (already installed)

These are automatically installed via Poetry when deploying the backend.

## Future Enhancements

For production deployment, consider integrating with:

- **SendGrid**: Professional email delivery service
- **AWS SES**: Amazon's Simple Email Service
- **Mailgun**: Email API service
- **Postmark**: Transactional email service

To integrate a production email service:

1. Update `app/email.py` with the new service's SMTP credentials
2. Replace the `send_vendor_welcome_email` function with the service's API
3. Update environment variables for API keys/credentials
4. Test thoroughly before deploying to production

## Troubleshooting

### Email not appearing in logs

- Ensure the backend is running and the vendor registration endpoint is being called
- Check that `print()` statements are being used (not just `logger.info()`)
- Verify the email function is being called in `app/main.py`

### Ethereal Email timeout

- The Ethereal SMTP service may be slow or unavailable
- Consider using Console Logging Mode for faster testing
- Check network connectivity and firewall settings

### Email content not formatted correctly

- Verify the HTML template in `app/email.py`
- Test with different email clients if using Ethereal
- Ensure all variables are being passed correctly

## Contact

For questions or issues with the email integration, contact the development team or refer to the main project documentation in `/home/ubuntu/blkxchange/README.md`.
