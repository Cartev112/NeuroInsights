# Setup Without Docker

## Local Development (No Docker)

### Prerequisites
- Python 3.11+
- Node.js 18+
- Git

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create `.env` file in backend directory:**
```bash
OPENAI_API_KEY=sk-your-openai-key-here
JWT_SECRET=your-secret-key-here
ENVIRONMENT=development
```

5. **Run the backend:**
```bash
uvicorn app.main:app --reload
```

Backend will run at: **http://localhost:8000**

API docs available at: **http://localhost:8000/docs**

### Frontend Setup

1. **Navigate to frontend directory (in a new terminal):**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Create `.env` file in frontend directory:**
```bash
VITE_API_URL=http://localhost:8000
```

4. **Run the frontend:**
```bash
npm run dev
```

Frontend will run at: **http://localhost:5173** or **http://localhost:3000**

### Access the Application

Open your browser to: **http://localhost:5173** (or the port shown in terminal)

## Railway Deployment

See **RAILWAY_DEPLOYMENT.md** for complete Railway deployment instructions.

### Quick Railway Deploy

1. **Push code to GitHub**

2. **Create Railway Project:**
   - Go to https://railway.app
   - New Project → Deploy from GitHub
   - Select your repository

3. **Deploy Backend:**
   - New Service → GitHub Repo
   - Root Directory: `backend`
   - Add environment variables:
     - `OPENAI_API_KEY`
     - `JWT_SECRET`
     - `ENVIRONMENT=production`

4. **Deploy Frontend:**
   - New Service → GitHub Repo
   - Root Directory: `frontend`
   - Add environment variable:
     - `VITE_API_URL=https://your-backend-url.up.railway.app`

5. **Done!** Both services will auto-deploy on push to GitHub.

## Troubleshooting

### Backend won't start

**"ModuleNotFoundError":**
```bash
# Make sure virtual environment is activated
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**"OpenAI API key not found":**
- Check `.env` file exists in `backend/` directory
- Verify `OPENAI_API_KEY` is set correctly
- No spaces around the `=` sign

### Frontend won't start

**"Cannot find module":**
```bash
# Delete node_modules and reinstall
rm -rf node_modules
npm install
```

**"Cannot connect to backend":**
- Make sure backend is running on port 8000
- Check `VITE_API_URL` in frontend `.env` file
- Verify URL is `http://localhost:8000` (no trailing slash)

### TypeScript errors in IDE

These are normal before running `npm install`. They will disappear after:
```bash
cd frontend
npm install
```

## Development Workflow

### Making Changes

1. **Backend changes:**
   - Edit files in `backend/app/`
   - FastAPI auto-reloads (if using `--reload` flag)
   - Check http://localhost:8000/docs for API changes

2. **Frontend changes:**
   - Edit files in `frontend/src/`
   - Vite auto-reloads in browser
   - Check browser console for errors

### Testing

**Backend:**
```bash
cd backend
pytest  # (when tests are added)
```

**Frontend:**
```bash
cd frontend
npm run lint
```

### Building for Production

**Backend:**
```bash
cd backend
# No build step needed - Python runs directly
```

**Frontend:**
```bash
cd frontend
npm run build
# Creates dist/ folder with optimized build
```

## Environment Variables Reference

### Backend (.env)
```bash
# Required
OPENAI_API_KEY=sk-your-key-here
JWT_SECRET=your-secret-key

# Optional
ENVIRONMENT=development
DATABASE_URL=postgresql://...  # If using database
REDIS_URL=redis://...          # If using Redis
```

### Frontend (.env)
```bash
# Required
VITE_API_URL=http://localhost:8000  # Local
# or
VITE_API_URL=https://your-backend.up.railway.app  # Production
```

## Next Steps

1. ✅ Set up local development environment
2. ✅ Test the application locally
3. 📖 Read RAILWAY_DEPLOYMENT.md for deployment
4. 🚀 Deploy to Railway
5. 🎉 Start using NeuroInsights!
