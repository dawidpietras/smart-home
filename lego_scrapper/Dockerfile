FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    cron \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

COPY scraper.cron /etc/cron.d/scraper-job

RUN chmod 0644 /etc/cron.d/scraper-job \
    && crontab /etc/cron.d/scraper-job

CMD ["cron", "-f"]