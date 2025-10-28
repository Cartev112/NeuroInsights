# Railway Deployment Guide

## Overview

This guide walks you through deploying NeuroInsights on Railway with two separate services:
1. **Backend** - FastAPI Python application
2. **Frontend** - Vite React application

## Prerequisites

- Railway account (https://railway.app)
- GitHub repository with your code
- OpenAI API key

## Deployment Steps

### 1. Create New Railway Project

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account and select the NeuroInsights repository

### 2. Deploy Backend Service

#### Create Backend Service

1. In your Railway project, click "New Service"
2. Select "GitHub Repo"
3. Choose your NeuroInsights repository
4. Set **Root Directory**: `backend`
5. Railway will auto-detect it as a Python app

#### Configure Backend Environment Variables

Add these environment variables to the backend service:

```
OPENAI_API_KEY=sk-your-openai-key-here
JWT_SECRET=your-random-secret-key-here
ENVIRONMENT=production
```

**Optional (Railway provides these automatically if you add databases):**
```
DATABASE_URL=postgresql://...  (if using PostgreSQL)
REDIS_URL=redis://...          (if using Redis)
```

#### Backend Settings

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Railway will automatically assign a PORT

#### Get Backend URL

After deployment, Railway will provide a URL like:
`https://your-backend-name.up.railway.app`

**Copy this URL - you'll need it for the frontend!**

### 3. Deploy Frontend Service

#### Create Frontend Service

1. In the same Railway project, click "New Service"
2. Select "GitHub Repo"
3. Choose your NeuroInsights repository again
4. Set **Root Directory**: `frontend`
5. Railway will auto-detect it as a Node.js app

#### Configure Frontend Environment Variables

Add this environment variable to the frontend service:

```
VITE_API_URL=https://your-backend-name.up.railway.app
```

Replace `your-backend-name.up.railway.app` with your actual backend URL from step 2.

#### Frontend Settings

- **Build Command**: `npm install && npm run build`
- **Start Command**: `npm run preview`
- Railway will automatically assign a PORT

### 4. Optional: Add Database Services

If you want to use PostgreSQL and Redis (for future features):

#### Add PostgreSQL

1. Click "New Service" in your project
2. Select "Database" → "PostgreSQL"
3. Railway automatically creates `DATABASE_URL` variable
4. This variable is automatically available to your backend service

#### Add Redis

1. Click "New Service" in your project
2. Select "Database" → "Redis"
3. Railway automatically creates `REDIS_URL` variable
4. This variable is automatically available to your backend service

### 5. Verify Deployment

1. **Backend Health Check**:
   - Visit: `https://your-backend-name.up.railway.app/health`
   - Should return: `{"status": "healthy"}`

2. **Backend API Docs**:
   - Visit: `https://your-backend-name.up.railway.app/docs`
   - Should show FastAPI Swagger UI

3. **Frontend**:
   - Visit: `https://your-frontend-name.up.railway.app`
   - Should load the NeuroInsights application

4. **Test Chat**:
   - Go to the Chat page
   - Try: "How was my focus today?"
   - Should get a response from GPT-4

## Project Structure on Railway

```
Railway Project: NeuroInsights
├── Backend Service (Python)
│   ├── Root Directory: backend/
│   ├── Environment: OPENAI_API_KEY, JWT_SECRET
│   └── URL: https://backend-xxx.up.railway.app
│
├── Frontend Service (Node.js)
│   ├── Root Directory: frontend/
│   ├── Environment: VITE_API_URL
│   └── URL: https://frontend-xxx.up.railway.app
│
├── PostgreSQL (Optional)
│   └── Auto-provides: DATABASE_URL
│
└── Redis (Optional)
    └── Auto-provides: REDIS_URL
```

## Environment Variables Summary

### Backend Service
| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `OPENAI_API_KEY` | ✅ Yes | Your OpenAI API key | `sk-...` |
| `JWT_SECRET` | ✅ Yes | Random secret for JWT | `your-secret-key` |
| `ENVIRONMENT` | ⚠️ Recommended | Set to "production" | `production` |
| `DATABASE_URL` | ❌ Optional | PostgreSQL connection | Auto-provided by Railway |
| `REDIS_URL` | ❌ Optional | Redis connection | Auto-provided by Railway |

### Frontend Service
| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `VITE_API_URL` | ✅ Yes | Backend API URL | `https://backend-xxx.up.railway.app` |

## Local Development

To run locally without Docker:

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt

# Create .env file with:
# OPENAI_API_KEY=sk-your-key
# JWT_SECRET=dev-secret

uvicorn app.main:app --reload
```

Backend runs at: http://localhost:8000

### Frontend
```bash
cd frontend
npm install

# Create .env file with:
# VITE_API_URL=http://localhost:8000

npm run dev
```

Frontend runs at: http://localhost:5173

## Troubleshooting

### Backend Issues

**"Module not found" errors:**
- Check that `requirements.txt` is in the backend directory
- Verify Railway is using the correct root directory: `backend`

**"OpenAI API key not found":**
- Verify `OPENAI_API_KEY` is set in Railway environment variables
- Check for typos in the variable name

**CORS errors:**
- Make sure frontend `VITE_API_URL` matches backend URL exactly
- Backend automatically allows Railway domains

### Frontend Issues

**"Cannot connect to backend":**
- Verify `VITE_API_URL` is set correctly
- Check backend is deployed and healthy
- Make sure URL doesn't have trailing slash

**Build fails:**
- Check Node.js version (should be 18+)
- Try clearing build cache in Railway settings

**Blank page after deployment:**
- Check browser console for errors
- Verify environment variables are set
- Check Railway logs for frontend service

### Database Issues

**"Cannot connect to database":**
- Verify PostgreSQL service is running
- Check `DATABASE_URL` is available to backend
- Railway automatically links services in same project

## Monitoring

### View Logs

1. Go to your Railway project
2. Click on a service (Backend or Frontend)
3. Click "Logs" tab
4. View real-time logs

### Check Metrics

1. Click on a service
2. Click "Metrics" tab
3. View CPU, Memory, Network usage

## Updating Your Deployment

Railway automatically redeploys when you push to GitHub:

1. Make changes to your code
2. Commit and push to GitHub
3. Railway detects changes and redeploys automatically

To manually redeploy:
1. Go to service in Railway
2. Click "Deploy" → "Redeploy"

## Cost Estimates

Railway pricing (as of 2024):
- **Hobby Plan**: $5/month
  - Includes $5 usage credit
  - Good for development/testing
  
- **Pro Plan**: $20/month
  - Includes $20 usage credit
  - Better for production

Typical usage for NeuroInsights:
- Backend: ~$3-5/month
- Frontend: ~$2-3/month
- PostgreSQL: ~$2-3/month (if used)
- Redis: ~$1-2/month (if used)

## Custom Domains (Optional)

To use your own domain:

1. Go to service settings in Railway
2. Click "Domains"
3. Click "Add Domain"
4. Follow instructions to configure DNS

## Security Best Practices

1. **Never commit API keys** to Git
2. **Use strong JWT_SECRET** in production
3. **Enable Railway's built-in SSL** (automatic)
4. **Regularly rotate secrets**
5. **Monitor logs** for suspicious activity

## Next Steps

After deployment:
1. Test all features thoroughly
2. Monitor logs for errors
3. Set up custom domain (optional)
4. Configure database backups (if using PostgreSQL)
5. Set up monitoring/alerting

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- NeuroInsights Issues: GitHub repository issues

---

**You're all set!** Your NeuroInsights application is now running on Railway. 🚀
