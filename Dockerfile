FROM python:3.14-slim

LABEL org.opencontainers.image.title="Kokos"
LABEL org.opencontainers.image.description="Telegram bot for TikTok and YouTube Shorts video replies"
LABEL org.opencontainers.image.source="https://github.com/Oleksii1221/Kokos"
LABEL org.opencontainers.image.licenses="MIT"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

CMD ["python", "-m", "app.bot"]
