FROM python:3.11-slim-buster

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD bash /app/runserver.sh