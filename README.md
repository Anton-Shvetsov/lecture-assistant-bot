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

## Monitoring (Optional)

The bot logs usage statistics in `llm_client.log` which can be collected by Promtail and visualized with Grafana.

### SetUp

```
docker-compose up -d
```

### Navigation

Dashboard UI is accessible at `http://localhost:3000` (default user: `admin`, password: `admin`)

Dashboards -> Lecture Assistant -> Lecture Assistant Analytics

### Metrics

The Lecture Assistant Analytics dashboard shows:

- **Subjects popularity**: pie chart of most accessed subjects.
- **Top lectures per subject**: pie chart filtered by the selected subject.
- **Hashed tokens (cache_hit)**: total tokens served from cache.
- **Prompt raw tokens (cache_miss)**: total tokens processed by the model as new input.
- **Completion tokens**: total tokens returned by the model.
- **Total tokens**: sum of all tokens used (cache + new).
