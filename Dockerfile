FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1


WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . /app/
