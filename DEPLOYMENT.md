# BlkXchange™ Deployment Guide

## Prerequisites

Before deploying, ensure you have:
- Fly.io account (for backend)
- Vercel account (for frontend) or use the built-in deployment tool
- Environment variables configured

## Backend Deployment (FastAPI to Fly.io)

### Using Built-in Deployment Tool

The easiest way to deploy the backend is using the built-in deployment command:

```bash
# From the project root
deploy backend --dir=/home/ubuntu/blkxchange/blkxchange-backend
```

This will:
1. Package your FastAPI application
2. Deploy to Fly.io
3. Return a public URL for your backend API

### Manual Deployment (Alternative)

If you prefer manual deployment:

1. Install Fly CLI:
```bash
curl -L https://fly.io/install.sh | sh
```

2. Login to Fly:
```bash
fly auth login
```

3. Create a new app:
```bash
cd blkxchange-backend
fly launch
```

4. Deploy:
```bash
fly deploy
```

## Frontend Deployment (React to Vercel/Static Hosting)

### Using Built-in Deployment Tool

1. Build the frontend:
```bash
cd blkxchange-frontend
npm run build
```

2. Update the `.env` file with the deployed backend URL:
```bash
VITE_API_URL=https://your-backend-url.fly.dev
```

3. Rebuild with the new environment variable:
```bash
npm run build
```

4. Deploy:
```bash
# From project root
deploy frontend --dir=/home/ubuntu/blkxchange/blkxchange-frontend/dist
```

### Manual Deployment to Vercel (Alternative)

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Build the frontend:
```bash
cd blkxchange-frontend
npm run build
```

3. Deploy:
```bash
vercel --prod
```

## Environment Variables

### Backend (.env in blkxchange-backend/)
```
# Currently using in-memory database, no env vars needed for MVP
# For production, add:
DATABASE_URL=postgresql://...
STRIPE_SECRET_KEY=sk_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### Frontend (.env in blkxchange-frontend/)
```
VITE_API_URL=https://your-backend-url.fly.dev
```

## Post-Deployment Checklist

- [ ] Backend is accessible at the Fly.io URL
- [ ] Frontend is accessible at the deployment URL
- [ ] Frontend can successfully call backend API endpoints
- [ ] All pages load correctly
- [ ] Vendor registration form works
- [ ] Products display in marketplace
- [ ] Professionals display in directory
- [ ] Impact stats load correctly

## Testing Deployed Application

1. Visit the frontend URL
2. Navigate through all pages:
   - Landing page
   - Marketplace
   - Professionals
   - Impact
   - About
   - Vendor Registration
3. Test vendor registration form
4. Verify API calls in browser DevTools Network tab

## Troubleshooting

### Backend Issues

**Problem**: Backend not responding
- Check Fly.io logs: `fly logs`
- Verify app is running: `fly status`
- Check health endpoint: `curl https://your-app.fly.dev/healthz`

**Problem**: CORS errors
- Ensure CORS middleware is configured in main.py (already done)
- Verify frontend is using correct backend URL

### Frontend Issues

**Problem**: API calls failing
- Check `.env` file has correct `VITE_API_URL`
- Verify backend URL is accessible
- Check browser console for errors

**Problem**: Blank page
- Check browser console for JavaScript errors
- Verify build completed successfully
- Check that all dependencies are installed

## Monitoring

### Backend Monitoring
```bash
# View logs
fly logs

# Check app status
fly status

# View metrics
fly dashboard
```

### Frontend Monitoring
- Use Vercel dashboard for analytics
- Monitor browser console for client-side errors
- Use Vercel Analytics for user insights

## Scaling

### Backend Scaling
```bash
# Scale to multiple instances
fly scale count 2

# Scale VM size
fly scale vm shared-cpu-2x
```

### Frontend Scaling
- Vercel automatically scales based on traffic
- No manual intervention needed

## Security Notes

- Backend CORS is currently set to allow all origins for development
- For production, restrict CORS to your frontend domain only
- Add rate limiting to API endpoints
- Implement proper authentication before production launch
- Use environment variables for all sensitive data
- Never commit API keys or secrets to git

## Cost Estimates

### Fly.io (Backend)
- Free tier: 3 shared-cpu-1x VMs with 256MB RAM
- Paid: ~$5-10/month for basic production setup

### Vercel (Frontend)
- Free tier: Unlimited deployments, 100GB bandwidth
- Paid: $20/month for Pro features

## Support

For deployment issues:
- Backend: Check Fly.io documentation
- Frontend: Check Vercel documentation
- Application: Review README.md and code comments
