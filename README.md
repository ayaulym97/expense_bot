# 💰 Expense Tracker Telegram Bot

A fully-featured Telegram bot for tracking personal expenses with automatic Google Sheets integration. Built with Python, aiogram 3.x, and Google Sheets API.

## ✨ Features

- **Easy Expense Tracking**: Add expenses with simple text messages
- **Google Sheets Integration**: All data automatically saved to Google Sheets
- **Statistics**: View spending by day, week, or month
- **Category Tracking**: Organize expenses by categories
- **Private Access**: Whitelist-based user authentication
- **User-Friendly**: Intuitive commands and helpful error messages

## 📋 Requirements

- Python 3.11+
- Telegram Bot Token
- Google Service Account with Sheets API access
- Google Sheets API enabled

## 🚀 Quick Start

### 1. Get Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Set Up Google Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Google Sheets API**:
   - Navigate to "APIs & Services" → "Library"
   - Search for "Google Sheets API"
   - Click "Enable"
4. Create Service Account:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "Service Account"
   - Fill in the service account details
   - Click "Create and Continue"
   - Skip optional steps and click "Done"
5. Create and Download Key:
   - Click on the created service account
   - Go to "Keys" tab
   - Click "Add Key" → "Create New Key"
   - Select "JSON" format
   - Download the file and save it as `credentials.json`

### 3. Share Google Sheet with Service Account

1. Open the downloaded `credentials.json`
2. Find the `client_email` field (looks like `your-service@project.iam.gserviceaccount.com`)
3. Create a new Google Sheet or open existing one
4. Click "Share" button
5. Add the service account email with "Editor" permissions
6. Note the sheet name (you'll need it for configuration)

### 4. Install Dependencies

```bash
# Clone or download the project
cd expense_bot

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 5. Configure Environment

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` file with your credentials:
```env
TELEGRAM_TOKEN=your_bot_token_here
GOOGLE_SHEET_NAME=Expense Tracker
GOOGLE_CREDENTIALS_PATH=credentials.json
ALLOWED_USERS=123456789,987654321
```

**To get your Telegram User ID:**
- Send a message to [@userinfobot](https://t.me/userinfobot)
- Copy your ID and add it to `ALLOWED_USERS`

### 6. Place Credentials File

Move your `credentials.json` file to the project directory:
```bash
expense_bot/
├── bot.py
├── credentials.json  ← Place here
├── .env
└── ...
```

### 7. Run the Bot

```bash
python bot.py
```

You should see:
```
2024-12-08 17:23:00 - __main__ - INFO - Bot is starting...
2024-12-08 17:23:00 - __main__ - INFO - Allowed users: {123456789}
2024-12-08 17:23:00 - __main__ - INFO - Bot commands set successfully
2024-12-08 17:23:00 - __main__ - INFO - Starting bot polling...
```

## 📱 How to Use

### Adding Expenses

**Format:** `category amount comment`

**Examples:**
```
food 2500 coffee at Starbucks
transport 500 taxi to work
shopping 15000 new shoes
entertainment 1200 movie tickets
```

**Quick Add (amount only):**
```
2500
```
The bot will ask for the category.

### Commands

- `/start` - Welcome message and instructions
- `/stats` - View statistics (today/week/month)
- `/categories` - List all available categories
- `/help` - Get help on how to use the bot

### Example Interaction

```
You: food 2500 coffee

Bot: ✅ Expense saved!
     Category: food
     Amount: 2500.00
     Comment: coffee

You: /stats

Bot: 📊 Your Expense Statistics

     📅 Today:
     Total: 2500.00 (1 expenses)
       • food: 2500.00

     📆 This Week:
     Total: 15000.00 (8 expenses)
       • food: 5000.00
       • transport: 3000.00
       • shopping: 7000.00

     📈 This Month:
     Total: 45000.00 (25 expenses)
       • food: 12000.00
       • transport: 8000.00
       • shopping: 15000.00
       • entertainment: 10000.00
```

## 📊 Google Sheets Format

The bot creates a spreadsheet with the following columns:

| Date | Category | Amount | Comment | User ID |
|------|----------|--------|---------|---------|
| 2024-12-08 17:30 | food | 2500 | coffee | 123456789 |
| 2024-12-08 18:15 | transport | 500 | taxi | 123456789 |

## 🏗️ Project Structure

```
expense_bot/
├── bot.py                 # Main bot initialization and startup
├── handlers.py            # Message and command handlers
├── google_service.py      # Google Sheets integration
├── validators.py          # Pydantic models for validation
├── config.py              # Configuration and settings
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create from .env.example)
├── .env.example          # Example environment file
├── credentials.json      # Google Service Account credentials
└── README.md             # This file
```

## 🔒 Security

- **Whitelist Protection**: Only users in `ALLOWED_USERS` can interact with the bot
- **Environment Variables**: Sensitive data stored in `.env` file
- **Service Account**: Google Sheets access via service account (no OAuth required)
- **Private Bot**: Unauthorized users are silently ignored

## 🛠️ Deployment Options

### Local Development
```bash
python bot.py
```

### Production (with systemd on Linux)

1. Create service file `/etc/systemd/system/expense-bot.service`:
```ini
[Unit]
Description=Expense Tracker Telegram Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/expense_bot
ExecStart=/path/to/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

2. Enable and start:
```bash
sudo systemctl enable expense-bot
sudo systemctl start expense-bot
sudo systemctl status expense-bot
```

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

Build and run:
```bash
docker build -t expense-bot .
docker run -d --name expense-bot --env-file .env expense-bot
```

### Cloud Platforms

- **Heroku**: Use `Procfile` with `worker: python bot.py`
- **Railway**: Connect GitHub repo and set environment variables
- **DigitalOcean**: Deploy on App Platform or Droplet
- **AWS EC2**: Run on t2.micro instance with systemd

## 🐛 Troubleshooting

### Bot doesn't respond
- Check if your user ID is in `ALLOWED_USERS`
- Verify `TELEGRAM_TOKEN` is correct
- Check bot logs for errors

### Google Sheets errors
- Verify `credentials.json` is in the correct location
- Check if service account email has access to the sheet
- Ensure Google Sheets API is enabled in Google Cloud Console

### "Spreadsheet not found" error
- Make sure the sheet name in `.env` matches exactly
- Share the sheet with the service account email
- Check service account has "Editor" permissions

### Import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Use Python 3.11 or higher
- Activate virtual environment if using one

## 📝 Default Categories

- food
- transport
- entertainment
- shopping
- health
- utilities
- education
- other

You can use any category name - the bot will track all unique categories automatically.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

This project is open source and available under the MIT License.

## 💡 Tips

1. **Backup your data**: Regularly export your Google Sheet
2. **Use descriptive comments**: Makes it easier to track expenses later
3. **Review statistics weekly**: Use `/stats` to monitor spending patterns
4. **Add multiple users**: Include family members in `ALLOWED_USERS`
5. **Customize categories**: Use categories that match your spending habits

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section
2. Review bot logs for error messages
3. Verify all configuration steps were completed
4. Ensure all dependencies are installed correctly

---

**Happy expense tracking! 💰📊**
