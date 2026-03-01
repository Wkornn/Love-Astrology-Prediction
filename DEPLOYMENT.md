# Deployment Guide

## Architecture
- **Frontend**: Vercel (React + TypeScript + Vite)
- **Backend**: Render (FastAPI + Python)
- **Database**: SQLite (file-based, persisted on Render disk)

---

## 🚀 Backend Deployment (Render)

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub

### Step 2: Deploy Backend
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `love-astrology-backend`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

### Step 3: Add Environment Variables
In Render dashboard → Environment:
```
GEMINI_API_KEY=AIzaSyA2dmT4Z_tpZ-TfoJOs1sUAI_ukUc2lZDk
```

### Step 4: Add Disk for SQLite
1. Go to **"Disks"** tab
2. Click **"Add Disk"**
3. Configure:
   - **Name**: `sqlite-data`
   - **Mount Path**: `/opt/render/project/src/backend/app/data`
   - **Size**: `1 GB` (free tier)

### Step 5: Deploy
- Click **"Create Web Service"**
- Wait 5-10 minutes for build
- Copy your backend URL: `https://love-astrology-backend.onrender.com`

---

## 🎨 Frontend Deployment (Vercel)

### Step 1: Create Vercel Account
1. Go to https://vercel.com
2. Sign up with GitHub

### Step 2: Deploy Frontend
1. Click **"Add New..."** → **"Project"**
2. Import your GitHub repository
3. Configure:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### Step 3: Add Environment Variable
In Vercel dashboard → Settings → Environment Variables:
```
VITE_API_URL=https://love-astrology-backend.onrender.com
```
(Replace with your actual Render backend URL)

### Step 4: Deploy
- Click **"Deploy"**
- Wait 2-3 minutes
- Your site will be live at: `https://your-project.vercel.app`

---

## 🔧 Post-Deployment

### Update Frontend .env (Local Development)
```bash
# frontend/.env
VITE_API_URL=https://love-astrology-backend.onrender.com
```

### Test the Deployment
1. Visit your Vercel URL
2. Try all 3 modes:
   - Mode 1: Single person reading
   - Mode 2: Celebrity matching
   - Mode 3: Couple compatibility

### Import Celebrity Data (Optional)
If database is empty, SSH into Render or use their shell:
```bash
cd backend
python3 import_to_db.py
```

---

## 🐛 Troubleshooting

### Backend Issues
- **500 Error**: Check Render logs for Python errors
- **Database not persisting**: Verify disk is mounted correctly
- **pyswisseph error**: Render should auto-compile C extensions

### Frontend Issues
- **API connection failed**: Check CORS settings in backend
- **404 on refresh**: Vercel rewrites should handle this (already configured)
- **Environment variable not working**: Redeploy after adding env vars

### CORS Configuration
Backend already has CORS enabled in `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update to your Vercel domain for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

For production, update to:
```python
allow_origins=["https://your-project.vercel.app"]
```

---

## 💰 Cost
- **Render Free Tier**: 750 hours/month (sleeps after 15min inactivity)
- **Vercel Free Tier**: Unlimited bandwidth for personal projects
- **Total**: $0/month

---

## 🔄 Continuous Deployment
Both platforms auto-deploy on git push:
- Push to `main` branch → Auto-deploys to production
- Create PR → Vercel creates preview deployment

---

## 📝 Notes
- Render free tier spins down after 15min inactivity (first request takes ~30s)
- SQLite data persists on Render disk (1GB free)
- Consider upgrading to PostgreSQL for production use
