# 🚀 SmartStudyHub Deployment Guide

## Option 1: Deploy to Render (Recommended - FREE)

### Step 1: Create GitHub Repository

1. Go to [github.com](https://github.com) and create a new repository
2. Name it: `smartstudyhub` (or any name you prefer)
3. Make it **Public** (required for Render free tier)
4. Don't initialize with README (we already have files)

### Step 2: Push Code to GitHub

Open Command Prompt in your project folder and run:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - SmartStudyHub"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/smartstudyhub.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Render

1. Go to [render.com](https://render.com) and sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select your `smartstudyhub` repository
5. Render will auto-detect the `render.yaml` configuration
6. Click **"Create Web Service"**

### Step 4: Wait for Deployment

- First deployment takes 2-3 minutes
- You'll see build logs in real-time
- Once done, you'll get a URL like: `https://smartstudyhub.onrender.com`

### Step 5: Access Your App

Visit your URL! Your app is now live on the internet. 🎉

---

## Option 2: Local Network Deployment (Quick Share)

If you just want to share with people on the same WiFi:

### Step 1: Find Your Local IP

```bash
# Windows
ipconfig

# Look for "IPv4 Address" (e.g., 192.168.1.5)
```

### Step 2: Update Flask App

Edit `backend/app.py` - change the last line to:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Step 3: Run the App

```bash
python backend/app.py
```

### Step 4: Share the URL

Others on your WiFi can access: `http://YOUR_IP:5000`

Example: `http://192.168.1.5:5000`

---

## Troubleshooting

### Render Deployment Issues

**Build fails:**
- Check that all files (requirements.txt, render.yaml) are pushed to GitHub
- Verify Python version in render.yaml matches your local version

**App crashes:**
- Check Render logs for errors
- Ensure all dependencies are in requirements.txt

### Local Network Issues

**Can't access from other devices:**
- Check Windows Firewall settings
- Ensure port 5000 is allowed
- Both devices must be on same WiFi network

---

## Free Tier Limits

**Render Free Tier:**
- ✅ 750 hours/month (more than enough)
- ✅ Automatic HTTPS
- ✅ Custom domain support
- ⚠️ Spins down after 15 min of inactivity (first request may be slow)

---

## Next Steps After Deployment

1. **Custom Domain** - Add your own domain in Render settings
2. **Environment Variables** - Add API keys if needed later
3. **Monitoring** - Check Render dashboard for usage stats
4. **Updates** - Push to GitHub, Render auto-deploys

---

## Support

- Render Docs: https://render.com/docs
- GitHub Help: https://docs.github.com
