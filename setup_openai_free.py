#!/usr/bin/env python3
"""
Interactive setup script for OpenAI FREE tier.
"""

import os
from pathlib import Path

print("=" * 60)
print("🎉 OpenAI FREE Tier Setup for MemSafe")
print("=" * 60)
print()
print("OpenAI offers $5 FREE credits for new accounts!")
print("No credit card required initially - perfect for students!")
print()

# Check if key already exists
env_path = Path('.env')
openai_key = None

if env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('OPENAI_API_KEY='):
                openai_key = line.split('=', 1)[1].strip()
                break

if openai_key and openai_key.startswith('sk-'):
    print(f"✅ Found existing OpenAI key: {openai_key[:15]}...")
    use_existing = input("Use existing key? (y/n): ").lower().strip()
    if use_existing == 'y':
        print("✅ Using existing key!")
        exit(0)

print()
print("📝 Step 1: Sign Up for FREE OpenAI Account")
print("-" * 60)
print()
print("1. Open this URL in your browser:")
print("   https://platform.openai.com/signup")
print()
print("2. Sign up with:")
print("   - Email, OR")
print("   - Google account, OR")
print("   - GitHub account")
print()
print("3. Verify your email (if using email signup)")
print()
input("Press Enter when you've signed up...")

print()
print("📝 Step 2: Get Your FREE API Key")
print("-" * 60)
print()
print("1. Go to: https://platform.openai.com/api-keys")
print()
print("2. Click 'Create new secret key'")
print()
print("3. Name it: memsafe (or anything you want)")
print()
print("4. Click 'Create secret key'")
print()
print("5. ⚠️  IMPORTANT: Copy the key NOW (you won't see it again!)")
print("   It starts with 'sk-' and is about 51 characters long")
print()

token = input("Paste your OpenAI API key here: ").strip()

if not token:
    print("❌ No key provided. Exiting.")
    exit(1)

if not token.startswith('sk-'):
    print("⚠️  Warning: OpenAI keys should start with 'sk-'. Continuing anyway...")
    print()

if len(token) < 20:
    print("⚠️  Warning: Key seems too short. Valid keys are usually 51+ characters.")
    print()

# Add to .env file
print()
print("📝 Step 3: Adding key to .env file...")

# Read existing .env if it exists
env_lines = []
if env_path.exists():
    with open(env_path, 'r') as f:
        env_lines = f.readlines()
    
    # Remove old OPENAI_API_KEY if it exists
    env_lines = [line for line in env_lines if not line.startswith('OPENAI_API_KEY=')]

# Add new key
env_lines.append(f'OPENAI_API_KEY={token}\n')

# Write back
with open(env_path, 'w') as f:
    f.writelines(env_lines)

print("✅ API key added to .env file!")
print()
print("=" * 60)
print("🎊 Setup Complete!")
print("=" * 60)
print()
print("Next steps:")
print("1. Run: streamlit run app/main.py")
print("2. In the app, select 'OpenAI (Free Tier Available!)'")
print("3. Choose 'GPT-3.5-turbo' (cheaper, uses less credits)")
print("4. Paste your C code and click Analyze!")
print()
print("💡 Tips:")
print("   - You have $5 free credits (enough for many analyses)")
print("   - GPT-3.5-turbo is cheaper than GPT-4o")
print("   - Check usage at: https://platform.openai.com/usage")
print()

