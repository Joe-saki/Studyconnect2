# StudyConnect - Deployment Guide for Render

## What Was Fixed

Your Django project now has proper Render deployment configuration:

### Files Created:
- **Procfile** - Defines how Render runs your app
- **render.yaml** - Complete Render service configuration
- **requirements.txt** - Python dependencies for Render
- **runtime.txt** - Specifies Python version (3.11.8)
- **.env.example** - Template for environment variables
- **.gitignore** - Prevents sensitive files from being committed

### Files Updated:
- **settings.py** - Now supports environment variables and PostgreSQL

---

## Deploying to Render

### Step 1: Connect Your GitHub Repository
1. Go to [https://render.com](https://render.com)
2. Sign in with your GitHub account
3. Click "New +" → "Web Service"
4. Select your repository: `Joe-saki/Studyconnect2`
5. Click "Connect"

### Step 2: Configure the Service
Fill in the following details:

| Setting | Value |
|---------|-------|
| **Name** | studyconnect |
| **Environment** | Python 3 |
| **Build Command** | `pip install -r requirements.txt && python manage.py collectstatic --noinput` |
| **Start Command** | `gunicorn studyconnect.wsgi:application --bind 0.0.0.0:$PORT` |
| **Plan** | Free (for testing) or Starter (for production) |

### Step 3: Add Environment Variables
In the Render dashboard, add these environment variables:

```
SECRET_KEY=<generate-a-new-secret-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.onrender.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.onrender.com
```

**To generate a new SECRET_KEY in Python:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 4: Choose Database
Render will automatically create a PostgreSQL database if you let it. You can also:
- Use Render's PostgreSQL (Recommended)
- Add `DATABASE_URL` environment variable with your external database URL

### Step 5: Deploy
Click "Create Web Service" - Render will automatically:
1. Install dependencies from `requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Collect static files
4. Start your Django app with gunicorn

---

## After Deployment

### View Logs
In Render dashboard → Your Service → Logs

### Common Issues

**Error: Can't open file 'manage.py'**
- ✅ **FIXED** - The Procfile and runtime.txt now tell Render where to find it

**Static files not loading**
- ✅ **FIXED** - WhiteNoise middleware is now configured in settings.py

**Database connection errors**
- ✅ **FIXED** - settings.py now uses `DATABASE_URL` environment variable

**502 Bad Gateway**
- Check logs in Render dashboard
- Ensure all environment variables are set
- Verify the database is connected and migrations ran

---

## Project Structure
```
studyconnect/
├── Procfile                 # ← Render process definition
├── render.yaml              # ← Render service config
├── runtime.txt              # ← Python version
├── requirements.txt         # ← Dependencies
├── .env.example             # ← Environment variable template
├── manage.py
├── db.sqlite3              # ← Local dev database
├── studyconnect/           # ← Django project settings
│   ├── settings.py         # ← Updated for production
│   ├── wsgi.py
│   └── urls.py
├── core/                   # ← Main app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
├── static/                 # ← CSS, JS, images
└── media/                  # ← User uploads
```

---

## Features Included
✅ Chat system with real-time messaging (2-second polling)  
✅ User authentication and profiles  
✅ Study session scheduling  
✅ File uploads for notes  
✅ Course management  
✅ Meeting coordination  
✅ Professional responsive UI  

---

## Database
- **Development**: SQLite (`db.sqlite3`)
- **Production**: PostgreSQL (on Render)

The app automatically detects which database to use based on the `DATABASE_URL` environment variable.

---

## Security Notes
- Change `SECRET_KEY` before deploying to production
- Set `DEBUG=False` in production
- Update `ALLOWED_HOSTS` with your actual domain
- Keep `.env` file in `.gitignore` (already configured)

---

## Support
If you encounter any issues:
1. Check Render dashboard logs
2. Verify all environment variables are set
3. Ensure requirements.txt has all dependencies
4. Check that database migrations completed successfully

Happy deploying! 🚀
