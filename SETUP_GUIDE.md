# 🛠️ Complete Setup Guide

Step-by-step guide to set up your Expense Tracker Telegram Bot.

## Prerequisites

- Python 3.11 or higher
- A Telegram account
- A Google account
- Basic command line knowledge

## Part 1: Telegram Bot Setup (5 minutes)

### Step 1: Create Your Bot

1. Open Telegram on your phone or desktop
2. Search for **@BotFather** (official Telegram bot)
3. Start a chat and send: `/newbot`
4. Follow the prompts:
   - **Bot name**: Choose a display name (e.g., "My Expense Tracker")
   - **Bot username**: Choose a unique username ending in 'bot' (e.g., "my_expense_tracker_bot")

### Step 2: Get Your Bot Token

After creating the bot, BotFather will send you a message containing:
```
Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

**⚠️ Keep this token secret!** Anyone with this token can control your bot.

### Step 3: Get Your Telegram User ID

1. Search for **@userinfobot** in Telegram
2. Start a chat and send any message
3. The bot will reply with your user ID (e.g., `123456789`)
4. Save this number - you'll need it for the whitelist

## Part 2: Google Sheets API Setup (10 minutes)

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Select a project"** → **"New Project"**
3. Enter project name: `expense-tracker-bot`
4. Click **"Create"**
5. Wait for project creation (about 30 seconds)

### Step 2: Enable Google Sheets API

1. In the Cloud Console, go to **"APIs & Services"** → **"Library"**
2. Search for: `Google Sheets API`
3. Click on **"Google Sheets API"**
4. Click **"Enable"**
5. Wait for activation

### Step 3: Create Service Account

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"Service Account"**
3. Fill in details:
   - **Service account name**: `expense-bot-service`
   - **Service account ID**: (auto-filled)
   - **Description**: `Service account for expense tracker bot`
4. Click **"Create and Continue"**
5. Skip optional steps:
   - Click **"Continue"** (skip role selection)
   - Click **"Done"** (skip user access)

### Step 4: Create and Download Credentials

1. In the **Credentials** page, find your service account
2. Click on the service account email (looks like `expense-bot-service@project-id.iam.gserviceaccount.com`)
3. Go to the **"Keys"** tab
4. Click **"Add Key"** → **"Create new key"**
5. Select **"JSON"** format
6. Click **"Create"**
7. A JSON file will download automatically
8. **Rename this file to `credentials.json`**

### Step 5: Create Google Sheet

1. Go to [Google Sheets](https://sheets.google.com/)
2. Click **"Blank"** to create a new spreadsheet
3. Name it: `Expense Tracker` (or any name you prefer)
4. **Important**: Note the exact name - you'll use it in configuration

### Step 6: Share Sheet with Service Account

1. Open the `credentials.json` file you downloaded
2. Find the line with `"client_email"`:
   ```json
   "client_email": "expense-bot-service@project-id.iam.gserviceaccount.com"
   ```
3. Copy this email address
4. In your Google Sheet, click **"Share"** button (top right)
5. Paste the service account email
6. Set permission to **"Editor"**
7. **Uncheck** "Notify people"
8. Click **"Share"**

## Part 3: Bot Installation (5 minutes)

### Step 1: Download Project Files

```bash
# Navigate to your projects directory
cd ~/Projects

# If you have the project files, navigate to the expense_bot directory
cd expense_bot
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

You should see:
```
Successfully installed aiogram-3.13.1 python-dotenv-1.0.1 gspread-6.1.2 google-auth-2.35.0 pydantic-2.9.2
```

### Step 4: Configure Environment

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` file:
```bash
# On macOS/Linux:
nano .env

# On Windows:
notepad .env
```

3. Fill in your credentials:
```env
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
GOOGLE_SHEET_NAME=Expense Tracker
GOOGLE_CREDENTIALS_PATH=credentials.json
ALLOWED_USERS=123456789
```

**Replace with your actual values:**
- `TELEGRAM_TOKEN`: Your bot token from BotFather
- `GOOGLE_SHEET_NAME`: Exact name of your Google Sheet
- `ALLOWED_USERS`: Your Telegram user ID (add multiple IDs separated by commas)

4. Save and close the file:
   - In nano: Press `Ctrl+X`, then `Y`, then `Enter`
   - In notepad: Click `File` → `Save`

### Step 5: Add Credentials File

1. Move your downloaded `credentials.json` to the project directory:
```bash
# If credentials.json is in Downloads:
mv ~/Downloads/credentials.json .

# Verify it's there:
ls -la credentials.json
```

### Step 6: Verify Setup

Check that you have all required files:
```bash
ls -la
```

You should see:
```
-rw-r--r--  .env
-rw-r--r--  .env.example
-rw-r--r--  .gitignore
-rw-r--r--  README.md
-rw-r--r--  bot.py
-rw-r--r--  config.py
-rw-r--r--  credentials.json  ← Important!
-rw-r--r--  google_service.py
-rw-r--r--  handlers.py
-rw-r--r--  requirements.txt
-rwxr-xr-x  run.sh
-rw-r--r--  validators.py
```

## Part 4: First Run (2 minutes)

### Option 1: Using the Run Script (Recommended)

```bash
./run.sh
```

### Option 2: Manual Start

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the bot
python bot.py
```

### Expected Output

If everything is configured correctly, you should see:
```
2024-12-08 17:30:00 - __main__ - INFO - Bot is starting...
2024-12-08 17:30:00 - __main__ - INFO - Allowed users: {123456789}
2024-12-08 17:30:00 - __main__ - INFO - Bot commands set successfully
2024-12-08 17:30:00 - __main__ - INFO - Starting bot polling...
```

## Part 5: Testing (3 minutes)

### Test 1: Start Command

1. Open Telegram
2. Find your bot (search for the username you created)
3. Send: `/start`
4. You should receive a welcome message

### Test 2: Add Expense

Send: `food 2500 coffee`

You should receive:
```
✅ Expense saved!
Category: food
Amount: 2500.00
Comment: coffee
```

### Test 3: Check Google Sheets

1. Open your Google Sheet
2. You should see a new row with your expense:
   | Date | Category | Amount | Comment | User ID |
   |------|----------|--------|---------|---------|
   | 2024-12-08 17:35 | food | 2500 | coffee | 123456789 |

### Test 4: View Statistics

Send: `/stats`

You should see your expense statistics.

## Troubleshooting

### Bot doesn't respond

**Problem**: Bot doesn't reply to messages

**Solutions**:
1. Check if bot is running (should see "Starting bot polling..." in terminal)
2. Verify your user ID is in `ALLOWED_USERS` in `.env`
3. Make sure you're messaging the correct bot
4. Check bot token is correct in `.env`

### Google Sheets errors

**Problem**: "Spreadsheet not found" error

**Solutions**:
1. Verify sheet name in `.env` matches exactly (case-sensitive)
2. Check service account email has access to the sheet
3. Make sure service account has "Editor" permissions
4. Verify `credentials.json` is in the correct location

**Problem**: "Permission denied" error

**Solutions**:
1. Re-share the sheet with service account email
2. Make sure you granted "Editor" access, not just "Viewer"
3. Check the service account email in credentials.json matches the one you shared with

### Import errors

**Problem**: `ModuleNotFoundError: No module named 'aiogram'`

**Solutions**:
1. Make sure virtual environment is activated:
   ```bash
   source venv/bin/activate
   ```
2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration errors

**Problem**: "TELEGRAM_TOKEN is not set"

**Solutions**:
1. Check `.env` file exists (not `.env.example`)
2. Verify no spaces around `=` in `.env`:
   ```
   TELEGRAM_TOKEN=your_token  ✅
   TELEGRAM_TOKEN = your_token  ❌
   ```
3. Make sure token is not in quotes

## Advanced Configuration

### Adding Multiple Users

Edit `.env`:
```env
ALLOWED_USERS=123456789,987654321,555555555
```

### Changing Sheet Name

1. Edit `.env`:
```env
GOOGLE_SHEET_NAME=My Custom Sheet Name
```

2. Make sure the sheet with this exact name exists and is shared with service account

### Custom Categories

Categories are created automatically when you use them. No configuration needed!

## Next Steps

1. ✅ Read [EXAMPLES.md](EXAMPLES.md) for usage examples
2. ✅ Check [README.md](README.md) for deployment options
3. ✅ Start tracking your expenses!

## Getting Help

If you encounter issues:
1. Check the error message in the terminal
2. Review this setup guide step by step
3. Verify all configuration files are correct
4. Check that all services (Telegram, Google Sheets) are accessible

## Security Checklist

- [ ] `.env` file is not committed to git (check `.gitignore`)
- [ ] `credentials.json` is not committed to git
- [ ] Bot token is kept secret
- [ ] Only trusted users are in `ALLOWED_USERS`
- [ ] Google Sheet is only shared with service account

---

**Setup complete! Happy expense tracking! 💰**
