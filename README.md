<p align="center">
  <img src="/assets/logo.png" width="240px" height="240px" />
</p>

# hushbot

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

### Custom Rules

Hushbot allows you to specify your own regex and corosponding action for that regex.

To configure a custom rule simply edit your `config.yaml` to include a custom rule like shown below:

```yaml
  rules:
    - block_b.t:
        pattern: "b.t"
        action: "alert"
```

or multiple rules:

```yaml
  rules:
    - block_a.t:
        pattern: "a.t"
        action: "alert"
    - block_b.t:
        pattern: "b.t"
        action: "ban"
```

*Accepted actions are "alert", "delete", "ban"*

This example will detect any three-letter word that starts with b and ends with t. Once detected it will run the alert action.

**Important functionality notice**

Hushbot will ALWAYS run your custom rules before running any built-in checks.

## Running

To run, simply create a `.env` using the `.env.example` file and run the following command.

```shell
docker-compose --env-file .env up
```

This will create a `redis` container and an `bot` container.
By default, this docker-compose exposes the redis default ports. Since this bot should not store any sensitive data this shouldn't be an issue. If you don't want it to expose it's ports simply edit the `docker-compose.yaml` file.
