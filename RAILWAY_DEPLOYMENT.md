# Railway Deployment Guide for OneHub

## Prerequisites
- Railway account (https://railway.app)
- GitHub repository connected to Railway
- Environment variables configured

## Deployment Steps

### 1. Connect Your GitHub Repository to Railway
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Connect your GitHub account and authorize Railway
5. Select the `blackhamster987/onehub` repository

### 2. Configure Environment Variables
In the Railway dashboard, set these environment variables:

```
SECRET_KEY=your-secure-random-key-here
DEBUG=False
ALLOWED_HOSTS=your-railway-domain.railway.app
DATABASE_URL=your-postgres-database-url
GROQ_API_KEY=your-groq-api-key
RAZOR_KEY_ID=your-razorpay-key-id
RAZOR_KEY_SECRET=your-razorpay-key-secret
```

### 3. Add PostgreSQL Database (Recommended)
1. In Railway dashboard, add a new service
2. Select PostgreSQL
3. Railway will automatically set DATABASE_URL

### 4. Update settings.py for Production Database
Replace the DATABASES section in `onehub/settings.py` with:

```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}
```

### 5. Deploy
- Push changes to GitHub
- Railway will automatically detect commits and deploy
- Monitor deployment in Railway dashboard

### 6. Run Migrations
Once deployed, run migrations via Railway:
```
python manage.py migrate
python manage.py collectstatic --noinput
```

## Environment Variables Explained

- **SECRET_KEY**: Generate a secure key for production
- **DEBUG**: Should be False in production
- **ALLOWED_HOSTS**: Your Railway domain
- **DATABASE_URL**: PostgreSQL connection string (auto-configured with Railway Postgres)
- **GROQ_API_KEY**: Your Groq API key for chatbot
- **RAZOR_KEY_ID/SECRET**: Razorpay payment processor keys

## Troubleshooting

### Static Files Not Loading
- Run `python manage.py collectstatic --noinput`
- Ensure WhiteNoise middleware is enabled in settings.py

### Database Migration Errors
- Check DATABASE_URL environment variable
- Ensure migrations are applied correctly

### API Keys Not Working
- Verify all API keys are set in Railway environment variables
- Check `.env` file locally doesn't get committed (it's in .gitignore)

## Production Checklist

✅ DEBUG = False
✅ ALLOWED_HOSTS configured
✅ SECRET_KEY from environment variable
✅ Database uses PostgreSQL in production
✅ Static files configured with WhiteNoise
✅ All API keys in environment variables
✅ HTTPS enabled (automatic with Railway)
✅ Requirements.txt updated with all dependencies

## Additional Commands

Start deployment:
```bash
git push origin main
```

Connect to production shell (if needed):
```bash
railway shell
```

View logs:
```bash
railway logs
```
