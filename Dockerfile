FROM python:3.11 AS builder

ENV PYTHONUNBUFFERED=1
ENV PATH="/py/bin:$PATH"

WORKDIR /app

EXPOSE 80

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    gettext \
    libc-dev \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libffi-dev \
    libssl-dev && \
    apt-get remove -y build-essential && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp

COPY ./requirements.txt /app
RUN /py/bin/pip install --no-cache-dir -r requirements.txt
RUN /py/bin/pip install gunicorn

COPY ./ /app

CMD ["gunicorn", "--bind", "0.0.0.0:80", "TaskTracker.wsgi:application"]
