FROM python:3.10.1-slim-buster

WORKDIR /app

RUN python3 -m venv .venv

COPY application/ /app/application

RUN /app/.venv/bin/pip install -r /app/requirements.txt

CMD [".venv/bin/python", "application/discord_bot/bot.py"]