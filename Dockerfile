FROM python:3.10-alpine3.13
LABEL maintainer="danlopatenco@gmail.com"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements/requirements.txt /tmp/requirements.txt
COPY . /app

WORKDIR /app
EXPOSE 8000

ARG DEV=true
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base musl-dev libffi-dev python3-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps

ENV PATH="/py/bin:$PATH"
