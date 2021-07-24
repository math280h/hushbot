![Logo](logo.png)

# About

Text moderation bot for Discord.

This bot was initially created for learning purposes and does not currently implement any advanced methods to detect text that should be moderated.

However, with that said, it should still catch the most obvious.

## Configuration

Hushbot works with two types of configurations.

1. Environment Variables
    1. This is used for e.g. the bot token. (See .env.example)
    
2. config.yaml
    1. This is used for more general bot configuration such as the staff role, prefix and what channels to use.

To create a configuration simply make a copy of `config.example.yaml` called `config.yaml` in the root directory of the app.

## Running

To run, simply create a `.env` using the `.env.example` file and run the following command.

```shell
docker-compose --env-file .env up
```

This will create a `redis` container and an `bot` container.
By default, this docker-compose exposes the redis default ports. Since this bot should not store any sensitive data this shouldn't be an issue. If you don't want it to expose it's ports simply edit the `docker-compose.yaml` file.
