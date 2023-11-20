FROM python:3.9-slim-bullseye

COPY . /app
WORKDIR /app

RUN ls
RUN pip install -r requirements.txt

ENV FLASK_APP=API
CMD python3 API.py