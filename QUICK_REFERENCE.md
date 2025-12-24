# 📋 Quick Reference Card

## 🚀 Quick Start

```bash
# 1. Setup
cp .env.example .env
# Edit .env with your credentials

# 2. Install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Run
python bot.py
# or
./run.sh
```

## 💬 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message and instructions |
| `/stats` | View statistics (today/week/month) |
| `/categories` | List all available categories |
| `/help` | Get help on usage |

## 📝 Expense Input Formats

| Format | Example | Description |
|--------|---------|-------------|
| `category amount comment` | `food 2500 coffee` | Full format |
| `category amount` | `transport 500` | Without comment |
| `amount` | `2500` | Bot asks for category |

## 📊 Default Categories

- `food` - Meals, groceries, dining
- `transport` - Taxi, fuel, public transport
- `entertainment` - Movies, games, subscriptions
- `shopping` - Clothes, electronics, general shopping
- `health` - Medical, pharmacy, fitness
- `utilities` - Bills, internet, phone
- `education` - Courses, books, training
- `other` - Miscellaneous expenses

## 🔧 Configuration Files

### `.env`
```env
TELEGRAM_TOKEN=your_bot_token
GOOGLE_SHEET_NAME=Expense Tracker
GOOGLE_CREDENTIALS_PATH=credentials.json
ALLOWED_USERS=123456789,987654321
```

### Required Files
- `credentials.json` - Google Service Account credentials
- `.env` - Environment variables
- All Python files from the project

## 📁 Project Structure

```
expense_bot/
├── bot.py              # Main bot file
├── handlers.py         # Command handlers
├── google_service.py   # Google Sheets integration
├── validators.py       # Data validation
├── config.py          # Configuration
├── requirements.txt   # Dependencies
├── .env              # Your credentials (create this)
├── credentials.json  # Google credentials (add this)
└── run.sh           # Quick start script
```

## 🔑 Getting Credentials

### Telegram Bot Token
1. Message @BotFather
2. Send `/newbot`
3. Follow instructions
4. Copy token

### Telegram User ID
1. Message @userinfobot
2. Copy your ID

### Google Credentials
1. [Google Cloud Console](https://console.cloud.google.com/)
2. Create project
3. Enable Google Sheets API
4. Create Service Account
5. Download JSON key
6. Share sheet with service account email

## 📈 Google Sheets Format

| Date | Category | Amount | Comment | User ID |
|------|----------|--------|---------|---------|
| 2024-12-08 17:30 | food | 2500 | coffee | 123456789 |

## ⚡ Common Commands

```bash
# Start bot
python bot.py

# Start with script
./run.sh

# Activate venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Check if running
ps aux | grep bot.py

# Stop bot
# Press Ctrl+C in terminal
```

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Bot doesn't respond | Check user ID in ALLOWED_USERS |
| Sheet not found | Verify sheet name and sharing |
| Import errors | Activate venv, reinstall requirements |
| Token error | Check TELEGRAM_TOKEN in .env |
| Permission denied | Share sheet with service account |

## 💡 Usage Tips

1. **Consistent Categories**: Use same names for better stats
2. **Meaningful Comments**: Add details for future reference
3. **Regular Reviews**: Check `/stats` weekly
4. **Batch Entry**: Add multiple expenses quickly
5. **Mobile Friendly**: Use short category names

## 🔒 Security Checklist

- [ ] `.env` not in git
- [ ] `credentials.json` not in git
- [ ] Bot token is secret
- [ ] Only trusted users in whitelist
- [ ] Sheet only shared with service account

## 📱 Example Usage Flow

```
You: /start
Bot: [Welcome message]

You: food 2500 coffee
Bot: ✅ Expense saved!

You: /stats
Bot: [Statistics for today/week/month]

You: /categories
Bot: [List of all categories]
```

## 🌐 Deployment Options

| Platform | Command/Method |
|----------|----------------|
| Local | `python bot.py` |
| systemd | Create service file |
| Docker | `docker build -t expense-bot .` |
| Heroku | `Procfile: worker: python bot.py` |
| Railway | Connect GitHub repo |

## 📞 Support Resources

- [README.md](README.md) - Full documentation
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup
- [EXAMPLES.md](EXAMPLES.md) - Usage examples
- [aiogram docs](https://docs.aiogram.dev/) - Bot framework
- [gspread docs](https://docs.gspread.org/) - Google Sheets API

---

**Keep this card handy for quick reference! 📌**
