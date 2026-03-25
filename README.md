# 💰 Telegram Expense Tracker Bot

A Telegram bot that tracks your daily expenses, stores them in a PostgreSQL database and Google Sheets, and provides an analytics dashboard.

## Features

- **Track Expenses** — Send a message like `Lunch 200` to log an expense
- **Auto-Categorize** — Expenses are auto-categorized (Food, Travel, Rent, Bills, Other)
- **Spending Summary** — Use `/summary` to view total spending
- **Google Sheets Sync** — All expenses are synced to a Google Sheet
- **Analytics Dashboard** — Web dashboard with charts at `/dashboard`

## Tech Stack

- **Bot Framework**: FastAPI (webhook-based)
- **Database**: PostgreSQL + SQLAlchemy
- **Sheets**: Google Sheets API via `gspread`
- **Charts**: Matplotlib + Pandas

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/telegram-expense-bot.git
cd telegram-expense-bot
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

| Variable | Description |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Bot token from [@BotFather](https://t.me/BotFather) |
| `DATABASE_URL` | PostgreSQL connection string |
| `GOOGLE_SHEETS_CREDENTIALS_FILE` | Path to your Google service account JSON |
| `GOOGLE_SHEET_NAME` | Name of your Google Sheet |

### 5. Set up Google Sheets credentials

1. Create a service account in [Google Cloud Console](https://console.cloud.google.com/)
2. Download the credentials JSON and save it as `credentials.json` in the project root
3. Share your Google Sheet with the service account email

### 6. Set up the database

Create a PostgreSQL database and the expenses table:

```sql
CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    description VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 7. Run the bot

```bash
python main.py
```

The server starts on port `8000` by default. Set up a webhook pointing to `https://your-domain/telegram`.

## Bot Commands

| Command | Description |
|---|---|
| `/start` | Welcome message and usage instructions |
| `/summary` | View total spending |
| `<item> <amount>` | Log an expense (e.g., `Lunch 200`) |

## License

MIT
