# Lecture Assistant Bot

A Telegram bot for answering questions based on academic lectures.
Users select a subject and a specific lecture, then receive context-aware responses powered by Deepseek.

## Installation

```
git clone https://github.com/Anton-Shvetsov/lecture-assistant-bot.git
cd lecture-assistant-bot
pip install -r requirements.txt
```

## SetUp

Create .env file:

```
TELEGRAM_TOKEN=<YOUR_TELEGRAM_TOKEN>
DEEPSEEK_API_KEY=<YOUR_DEEPSEEK_API_KEY>
DEEPSEEK_API_URL=https://api.deepseek.com/beta
```

Place lectures to the lectures folder:

```
lectures/
├── <subject1>/
│ ├── <lecture1>.txt
│ ├── <lecture2>.txt
│ └── ...
├── <subject2>/
│ ├── <lecture1>.txt
│ └── ...
└── ...
```

## Usage

Run

```
python main.py
```
