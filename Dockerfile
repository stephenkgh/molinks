# syntax=docker/dockerfile:1
FROM python:3.10-alpine
RUN set -eux; \
    addgroup -g 1000 stephenk; \
    adduser -D -u 1000 -G stephenk stephenk
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN set -eux; \
    chown -Rv stephenk:stephenk requirements.txt; \
    pip install -r requirements.txt
USER stephenk
