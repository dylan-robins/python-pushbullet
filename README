# python-pushbullet

A python module for interacting with the v2 Pushbullet API.

## Setup

This tool supposes that your Pushbullet API key is located in an environment variable or a `.env` file. To create a `.env` file, type the following:

```sh
➜ echo PUSHBULLET_API_KEY=<your-api-key-here> > .env
```

Make sure that you don't commit this file to Git: it contains your private API key.


## Usage:

```sh
➜ ./pushbullet_cli.py post \
>    --title "Hello World" \
>    --body "Lorem ipsum dolor sit amet, consectetur adipiscing elit."

➜ ./pushbullet_cli.py devices
Chrome               | chrome
Google Pixel 3a      | android
Firefox              | firefox

➜ ./pushbullet_cli.py post \
>    --title "Hello World" \
>    --body "Lorem ipsum dolor sit amet, consectetur adipiscing elit." \
>    --device "Google Pixel 3a"
```

