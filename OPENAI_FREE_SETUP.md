# 🎉 OpenAI FREE Tier Setup Guide

## Quick Setup (5 minutes)

### Step 1: Sign Up (FREE - No Credit Card!)

1. Go to: **https://platform.openai.com/signup**
2. Sign up with:
   - Email, OR
   - Google account, OR  
   - GitHub account
3. Verify your email (if using email)

**✅ No credit card required for free tier!**

### Step 2: Get Your FREE API Key

1. Go to: **https://platform.openai.com/api-keys**
2. Click **"Create new secret key"**
3. Name it: `memsafe` (or anything)
4. Click **"Create secret key"**
5. **⚠️ COPY IT NOW** - you won't see it again!
   - It starts with `sk-`
   - About 51 characters long

### Step 3: Add to Your App

**Option A: Use the setup script (easiest)**
```bash
python3 setup_openai_free.py
```

**Option B: Manual setup**
1. Open your `.env` file:
   ```bash
   nano .env
   # or
   open -e .env
   ```

2. Add this line (replace with your actual key):
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

3. Save the file

### Step 4: Run the App!

```bash
streamlit run app/main.py
```

In the app:
- Select **"OpenAI (Free Tier Available!)"** provider
- Choose **"GPT-3.5-turbo"** (cheaper, uses less credits)
- Paste your C code and click **Analyze**!

## What You Get

- **$5 FREE credits** (no credit card needed initially)
- Enough for **many code analyses**
- Works immediately - no waiting!

## Cost Breakdown

| Model | Cost per 1M tokens | Your $5 gets you |
|-------|-------------------|-----------------|
| GPT-3.5-turbo | ~$0.50-1.50 | ~3-10M tokens |
| GPT-4o | ~$2.50-10 | ~0.5-2M tokens |

**Recommendation**: Use GPT-3.5-turbo - it's much cheaper and works great for code analysis!

## Check Your Usage

Visit: https://platform.openai.com/usage

See exactly how much you've used and how much is left.

## Troubleshooting

**Key not working?**
- Make sure you copied the full key (starts with `sk-`, ~51 chars)
- Check there are no extra spaces in `.env` file
- Restart the Streamlit app after adding the key

**Out of credits?**
- Check usage: https://platform.openai.com/usage
- Free tier credits don't renew automatically
- You'd need to add billing to continue (but $5 should last a while!)

## That's It! 🎊

You're all set! The app will work perfectly with OpenAI's free tier.

