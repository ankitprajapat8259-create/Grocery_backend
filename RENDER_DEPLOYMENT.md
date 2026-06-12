# Render Deployment Guide for Django Backend

## Overview
This guide explains how to deploy your Django REST API backend to Render with proper configuration for both development and production environments.

## Prerequisites
- Render account (https://render.com)
- GitHub repository with your backend code
- Vercel frontend URL (for CORS/CSRF configuration)

## Step 1: Create PostgreSQL Database on Render

1. Go to Render Dashboard → New → PostgreSQL
2. Choose a name (e.g., `grocery-db`)
3. Select database version (PostgreSQL 14+ recommended)
4. Choose region closest to your users
5. Click "Create Database"

**Important:** Save the database connection details from Render dashboard:
- Internal Database URL
- External Database URL
- Database Name
- Database User
- Database Password
- Database Host
- Database Port

## Step 2: Create Web Service on Render

1. Go to Render Dashboard → New → Web Service
2. Connect your GitHub repository
3. Configure the following settings:

### Build & Deploy Settings

**Runtime:** Python 3

**Build Command:**
```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

**Start Command:**
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

**Environment Variables:** (See Step 3)

## Step 3: Configure Environment Variables

Add these environment variables in your Render Web Service:

### Django Settings
```
DJANGO_SECRET_KEY=your-very-secure-secret-key-here-use-django-secrets-generator
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
```

### Database Settings (from your PostgreSQL database)
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=your-database-host.onrender.com
DB_PORT=5432
```

### CORS Settings (your Vercel frontend URL)
```
CORS_ALLOWED_ORIGINS=https://your-vercel-app.vercel.app,https://your-custom-domain.com
```

### CSRF Settings (your Vercel frontend URL)
```
CSRF_TRUSTED_ORIGINS=https://your-vercel-app.vercel.app,https://your-custom-domain.com
```

## Step 4: Update Vercel Frontend Environment Variables

In your Vercel frontend project, update the API base URL to point to your Render backend:

```
VITE_API_URL=https://your-app-name.onrender.com/api
```

## Step 5: Local Development Setup

For local development, create a `.env` file in your backend directory:

```bash
# Django Settings
DJANGO_SECRET_KEY=django-insecure-dev-key-only
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings (local MySQL)
DB_NAME=grocery_db
DB_USER=root
DB_PASSWORD=root123
DB_HOST=localhost
DB_PORT=3306

# CORS Settings (local React dev server)
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## Step 6: Verify Deployment

1. Check Render dashboard for deployment status
2. Visit your Render URL: `https://your-app-name.onrender.com`
3. Test API endpoints: `https://your-app-name.onrender.com/api/`
4. Check logs in Render dashboard for any errors

## Security Notes

### Production Security
- Never set `DEBUG=True` in production
- Use a strong `DJANGO_SECRET_KEY` (generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- Always use HTTPS (Render provides SSL certificates automatically)
- Keep database credentials secure
- Regularly update dependencies

### CORS and CSRF
- `CORS_ALLOW_ALL_ORIGINS` is automatically set to `False` in production
- Only add your actual Vercel frontend domains to `CORS_ALLOWED_ORIGINS`
- Only add your actual Vercel frontend domains to `CSRF_TRUSTED_ORIGINS`
- Both settings support comma-separated multiple domains

## Troubleshooting

### Common Issues

**1. CORS Errors**
- Verify `CORS_ALLOWED_ORIGINS` includes your Vercel frontend URL
- Check that the URL starts with `https://` for production
- Ensure no trailing slashes in URLs

**2. CSRF Errors**
- Verify `CSRF_TRUSTED_ORIGINS` includes your Vercel frontend URL
- Check that the URL starts with `https://` for production
- Ensure your frontend sends CSRF token in requests

**3. Database Connection Errors**
- Verify database credentials match Render PostgreSQL settings
- Check that database is in the same region as your web service
- Ensure database is not in a suspended state

**4. Static Files Not Loading**
- Verify `collectstatic` ran during build
- Check WhiteNoise is properly configured in settings.py
- Ensure `STATIC_ROOT` is set correctly

**5. 502 Bad Gateway**
- Check that gunicorn is running on the correct port
- Verify start command is correct
- Check application logs for startup errors

## Additional Configuration

### Custom Domain (Optional)
1. Add custom domain in Render dashboard
2. Update `ALLOWED_HOSTS` to include custom domain
3. Update `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS`
4. Configure DNS records as instructed by Render

### Database Backups
- Render automatically backs up PostgreSQL databases
- Configure backup retention in Render dashboard
- Consider manual backups before major changes

### Monitoring
- Enable Render monitoring for your web service
- Set up alerts for errors and performance issues
- Review logs regularly

## Cost Considerations

- Render Free Tier: Limited resources, spins down when inactive
- Render Starter: $7/month, always available
- PostgreSQL Free Tier: 90 days, then paid tiers available
- Consider your expected traffic when choosing plans

## Support

For issues specific to:
- Django: Check Django documentation
- Render: Check Render documentation and support
- This project: Review code and configuration files
