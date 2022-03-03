FROM python:3.10.1-slim-buster

WORKDIR /app

RUN python3 -m venv .venv

COPY application/ /app/application
COPY setup/ /app/setup

RUN /app/.venv/bin/pip install -r /app/setup/requirements.txt

CMD ["/app/.venv/bin/python", "/app/application/scripts/lambda.py"]