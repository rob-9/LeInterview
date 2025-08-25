# Deployment Guide

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

3. Run the application:
```bash
python app.py
```

## Heroku Deployment

1. Install Heroku CLI and login:
```bash
heroku login
```

2. Create a new Heroku app:
```bash
heroku create your-app-name
```

3. Set environment variables:
```bash
heroku config:set GEMINI_API_KEY=your_api_key_here
```

4. Deploy:
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## Docker Deployment

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. Set environment variables in `.env` file before running.

## Railway Deployment

1. Connect your GitHub repository to Railway
2. Set the GEMINI_API_KEY environment variable in Railway dashboard
3. Deploy automatically on push to main branch

## Vercel Deployment

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel --prod
```

3. Set environment variables in Vercel dashboard

## Environment Variables Required

- `GEMINI_API_KEY`: Your Google Gemini API key
- `FLASK_ENV`: Set to `production` for production deployment
- `PORT`: Port number (automatically set by most platforms)

## Post-Deployment Setup

1. Test all features:
   - Speech recognition
   - AI feedback
   - Code execution
   - Question generation

2. Monitor logs for any errors
3. Set up SSL certificate (handled automatically by most platforms)