FROM python:3.10.1-slim-buster

WORKDIR /app

RUN python3 -m venv .venv

COPY *.py .
COPY .env .
COPY requirements.txt .

RUN .venv/bin/pip install -r requirements.txt

CMD [".venv/bin/python", "bot.py"]