# 📖 Usage Examples

This document provides detailed examples of how to use the Expense Tracker Bot.

## 🎯 Basic Usage

### Adding Expenses

#### Example 1: Full Format
```
User: food 2500 coffee at Starbucks

Bot: ✅ Expense saved!
     Category: food
     Amount: 2500.00
     Comment: coffee at Starbucks
```

#### Example 2: Without Comment
```
User: transport 500

Bot: ✅ Expense saved!
     Category: transport
     Amount: 500.00
```

#### Example 3: Amount Only (Interactive)
```
User: 3500

Bot: 💰 Amount: 3500.00
     
     Please send the category for this expense.
     
     Examples: food, transport, entertainment, shopping, health

User: shopping

Bot: ✅ Expense saved!
     Category: shopping
     Amount: 3500.00
```

## 📊 Statistics Examples

### Daily Statistics
```
User: /stats

Bot: 📊 Your Expense Statistics

     📅 Today:
     Total: 8500.00 (4 expenses)
       • food: 5000.00
       • transport: 1500.00
       • shopping: 2000.00

     📆 This Week:
     Total: 45000.00 (18 expenses)
       • food: 15000.00
       • shopping: 12000.00
       • transport: 8000.00
       • entertainment: 6000.00
       • health: 4000.00

     📈 This Month:
     Total: 125000.00 (67 expenses)
       • shopping: 35000.00
       • food: 30000.00
       • transport: 20000.00
       • entertainment: 15000.00
       • health: 12000.00
       • utilities: 8000.00
       • education: 5000.00
```

## 📂 Categories Examples

### Viewing Categories
```
User: /categories

Bot: 📂 Available categories:

     • education
     • entertainment
     • food
     • health
     • other
     • shopping
     • transport
     • utilities
```

## 💡 Real-World Scenarios

### Scenario 1: Morning Coffee Run
```
User: food 350 cappuccino

Bot: ✅ Expense saved!
     Category: food
     Amount: 350.00
     Comment: cappuccino
```

### Scenario 2: Taxi to Work
```
User: transport 450 taxi to office

Bot: ✅ Expense saved!
     Category: transport
     Amount: 450.00
     Comment: taxi to office
```

### Scenario 3: Grocery Shopping
```
User: food 8500 weekly groceries at supermarket

Bot: ✅ Expense saved!
     Category: food
     Amount: 8500.00
     Comment: weekly groceries at supermarket
```

### Scenario 4: Movie Night
```
User: entertainment 1200 cinema tickets

Bot: ✅ Expense saved!
     Category: entertainment
     Amount: 1200.00
     Comment: cinema tickets
```

### Scenario 5: Utility Bill
```
User: utilities 3500 electricity bill

Bot: ✅ Expense saved!
     Category: utilities
     Amount: 3500.00
     Comment: electricity bill
```

### Scenario 6: Medical Expenses
```
User: health 2500 pharmacy

Bot: ✅ Expense saved!
     Category: health
     Amount: 2500.00
     Comment: pharmacy
```

### Scenario 7: Online Course
```
User: education 15000 Python course subscription

Bot: ✅ Expense saved!
     Category: education
     Amount: 15000.00
     Comment: Python course subscription
```

## ❌ Error Handling Examples

### Invalid Format
```
User: this is not valid

Bot: ❌ Invalid format. Expected: category amount [comment]

     Use: category amount comment
     Example: food 2500 coffee

     Or send /help for more info.
```

### Invalid Amount
```
User: food abc coffee

Bot: ❌ Invalid amount: abc

     Use: category amount comment
     Example: food 2500 coffee
```

### Unauthorized User
```
User (not in whitelist): /start

Bot: (no response - silently ignored)
```

## 🔄 Complete Workflow Example

```
User: /start

Bot: 👋 Welcome to Expense Tracker Bot!

     I'll help you track your expenses and save them to Google Sheets.

     How to add an expense:
     Send a message in this format:
     category amount comment

     Examples:
     • food 2500 coffee at Starbucks
     • transport 500 taxi
     • shopping 15000 new shoes

     You can also send just a number, and I'll ask for the category.

     Available commands:
     /start - Show this message
     /stats - View your statistics
     /categories - List all categories
     /help - Get help

     Let's start tracking! 💰

User: food 350 breakfast

Bot: ✅ Expense saved!
     Category: food
     Amount: 350.00
     Comment: breakfast

User: transport 200

Bot: ✅ Expense saved!
     Category: transport
     Amount: 200.00

User: 1500

Bot: 💰 Amount: 1500.00
     
     Please send the category for this expense.
     
     Examples: food, transport, entertainment, shopping, health

User: shopping

Bot: ✅ Expense saved!
     Category: shopping
     Amount: 1500.00

User: /stats

Bot: 📊 Your Expense Statistics

     📅 Today:
     Total: 2050.00 (3 expenses)
       • shopping: 1500.00
       • food: 350.00
       • transport: 200.00

     📆 This Week:
     Total: 2050.00 (3 expenses)
       • shopping: 1500.00
       • food: 350.00
       • transport: 200.00

     📈 This Month:
     Total: 2050.00 (3 expenses)
       • shopping: 1500.00
       • food: 350.00
       • transport: 200.00
```

## 📱 Mobile Usage Tips

1. **Quick Entry**: Use short category names for faster typing
   ```
   food 500 lunch
   ```

2. **Voice Input**: Use Telegram's voice-to-text feature
   - Tap microphone icon
   - Say: "food 2500 coffee"
   - Send message

3. **Saved Messages**: Save common expense formats
   - Save to "Saved Messages"
   - Copy and modify amounts as needed

4. **Shortcuts**: Create keyboard shortcuts on iOS/Android
   - `fe` → `food [amount] `
   - `te` → `transport [amount] `

## 🎨 Category Suggestions

### Food & Dining
- `food 350 breakfast`
- `food 800 lunch`
- `food 1200 dinner`
- `food 250 snacks`
- `food 500 coffee`

### Transportation
- `transport 200 bus`
- `transport 500 taxi`
- `transport 3000 fuel`
- `transport 150 parking`

### Shopping
- `shopping 5000 clothes`
- `shopping 8000 groceries`
- `shopping 2500 electronics`
- `shopping 1500 books`

### Entertainment
- `entertainment 1000 movie`
- `entertainment 3000 concert`
- `entertainment 500 games`
- `entertainment 2000 streaming subscriptions`

### Health
- `health 2500 pharmacy`
- `health 5000 doctor visit`
- `health 1500 vitamins`
- `health 3000 gym membership`

### Utilities
- `utilities 3500 electricity`
- `utilities 2000 water`
- `utilities 1500 internet`
- `utilities 800 phone`

### Education
- `education 15000 course`
- `education 2500 books`
- `education 5000 certification`
- `education 1000 workshop`

## 🔍 Pro Tips

1. **Be Consistent**: Use the same category names for better statistics
2. **Add Details**: Include meaningful comments for future reference
3. **Regular Reviews**: Check `/stats` weekly to monitor spending
4. **Custom Categories**: Create categories that match your lifestyle
5. **Batch Entry**: Add multiple expenses at once by sending separate messages

---

**Happy tracking! 💰**
