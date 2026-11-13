# VIT Typing Club Discord Bot

A Discord bot for the VIT Typing Club

## Requirements

- Python 3.14.0
- Discord Bot Token

## Setup

```bash
git clone https://github.com/vit-typing-club/typingstats-vit-discordbot.git
cd typing-club-discord

# Create virtual environment
python3.14 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=your_discord_channel_id
API_URL=http://127.0.0.1:5000/api/scores/typegg/daily
TIMEZONE=Asia/Kolkata
```

## Run

```bash
python bot.py
```