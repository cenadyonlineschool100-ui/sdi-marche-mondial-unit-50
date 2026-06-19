FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY . /app

RUN mkdir -p /app/sdi_market/staticfiles /app/sdi_market/media

ENV DJANGO_SETTINGS_MODULE=sdi_market.settings
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "sdi_market.asgi:application"]
