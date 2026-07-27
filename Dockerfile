# 🌀 Scraper Quântico — Nano/Pico 🪶
# Sem browser, sem Chromium, sem selenium
# Só trafilatura + fastapi = extração limpa

FROM python:3.13-alpine3.21

WORKDIR /app

RUN apk add --no-cache wget ca-certificates

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

RUN adduser -D scraper
USER scraper

ENV HOST=0.0.0.0
ENV PORT=8000

EXPOSE 8000

HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]