FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

ENV PYTHONUNBUFFERED 1
WORKDIR /app

RUN apt-get update && apt-get install -y netcat-traditional \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp


COPY . /app/


RUN chmod +x /app/entrypoint.sh


ENTRYPOINT ["/app/entrypoint.sh"]


CMD []