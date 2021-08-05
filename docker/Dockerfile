FROM python:3.9.1

WORKDIR /bot

# Handle Requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Entrypoint
COPY docker/entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]

# Copy Configuration
COPY config.yaml config.yaml

# Copy Code
RUN touch bot.log
COPY src src
COPY run.py run.py