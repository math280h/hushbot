FROM python:3.9

WORKDIR /bot

# Copy Code
COPY src src
COPY run.py run.py
COPY bot.log bot.log

# Copy Configuration
COPY config.yaml config.yaml

# Handle Requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Entrypoint
COPY entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]