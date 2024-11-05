FROM python:3.10-slim-bullseye

WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2


COPY requirements.txt .
RUN pip install -r requirements.txt

COPY jobs_project/ ./jobs_project/
COPY infra/ ./infra/

ENV PYTHONPATH=/app


COPY data_source/ ./data_source/

COPY . .


CMD ["sh", "-c", "sleep 3 && cd jobs_project/jobs_project/spiders && scrapy runspider json_spider.py && cd /app && python query.py"]


