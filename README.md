# ![Marvin](https://user-images.githubusercontent.com/5514990/53703935-bc0cc900-3e49-11e9-9d9e-952101a4c0cf.png) Marvin

> Marvin, more fully known as Marvin the *Paranoid Android*, is an incredibly brilliant but overwhelmingly depressed robot manufactured by the **Sirius Cybernetics Corporation** and unwilling servant to the crew of the *Heart of Gold*.

## No seriously, what is Marvin?

Marvin is a **Slack Bot layout** for *Flask* and *Asyncio* to develop [*Slack* Event](https://api.slack.com/events) handlers and deploy on *AWS Lambda* + *API Gateway*.


## Create a Slack bot user

See the [Slack's documentation](https://api.slack.com/bot-users#getting-started) for further guidance on creating your bot (**step 1**).

Within the *Basic Information* about your application, copy the **Signing Secret** necessary to [verify requests from Slack](https://api.slack.com/docs/verifying-requests-from-slack>).

![Signing Secret](https://user-images.githubusercontent.com/5514990/53696736-cfde0e00-3dfc-11e9-9aeb-23d184f8c600.png)

Now go to the *OAuth & Permissions* section and copy the **Bot User OAuth Access Token** to configure the Bot's credentials.

![OAuth](https://user-images.githubusercontent.com/5514990/53776565-fc8f4400-3f28-11e9-9d7f-f4f24809c5e0.png)


## Configure your Application

Fill in your `.env` file with your `SLACK_SIGNING_SECRET` and `SLACK_API_TOKEN` keys obtained in the previous **step 1**

```sh
$ cp .env.example .env
```

🐣 Build the local environment:

```sh
$ make up
```

To avoid cyclic calls between subscriptions and API calls, set the Slack variables that identify your Bot:

```sh
$ make botinfo
```

```
{
    "id": "AGOAULRCZ",
    "name": "marvin",
    "profile": {
        "bot_id": CGK8R9V7S",
    },
    "is_bot": true
}
```

Copy the `id` value for `SLACK_BOT_USER_ID` and the `bot_id` value for `SLACK_BOT_ID` from your `.env` file and reload the Docker container.

```sh
$ make reload
```

🚀 Run your local server:

```sh
$ make run
```

Finally, you need a **Public URL** to subscribe to *Slack* events, you can use [ngrok](https://ngrok.com/download) to create a tunnel to development server and get your public url:


```sh
$ make ngrok
```

![ngrok](https://user-images.githubusercontent.com/5514990/53827525-ec6d7800-3fad-11e9-92c1-a912b2241e1f.png)

As you can see in the image, *ngrok* has assigned to the development server a subdomain `dd15a495`, so the Public URL is `https://dd15a495.ngrok.io/api/v1/slack/events`.

## Configure your Slack Bot

Continue with the [Slacks's documentation](https://api.slack.com/bot-users#setup-events-api) to setting up the Events API (**step 2**) and enter the URL to receive the subscriptions:

![Enable Events](https://user-images.githubusercontent.com/5514990/53777794-1df22f00-3f2d-11e9-85bd-03dcb9c9c848.png)

Select the [Slack Events](https://api.slack.com/events) you want to subscribe to, these events are required for the code examples in your project's `app/handlers` directory.

![Suscribe to bot Event](https://user-images.githubusercontent.com/5514990/53778614-f0f34b80-3f2f-11e9-96de-3cb2d1a8e0c3.png)

Finally, install your bot to a workspace (**step 3**).


## AWS Lambda Deployment

Install [AWS Command Line Interface](https://docs.aws.amazon.com/es_es/cli/latest/userguide/cli-chap-install.html) and configure the *marvin* profile

```sh
$ pip install awscli --upgrade --user
$ aws configure --profile marvin
```

Then create a zappa configuration file `zappa_settings.json` and upload your `config.json` file to your s3 bucket using the same url as the `remote_env` field from your `zappa_settings.json`.

Build your λ docker container:

```sh
$ make lambda
```

Here we go!

```sh
$ make zappa cmd=deploy
```

## Available Commands

```sh
$ make help
```

```
Please use 'make <target>' where <target> is one of
  build         Build docker image
  up            Run docker container and build if the image does not exist
  restart       Restart docker container
  rm            Remove docker container
  reload        Reload docker container
  logs          View output from docker container
  sh            Run bash shell on the container
  ngrok         Create a tunnel to development server
  run           Run a local development server
  botinfo       Show the current Bot info
  requirements  Install pip requirements from $REQUIREMENTS_FILES variable
  lambda        Build λ docker container
  zappa         Run zappa command (usage: make zappa cmd={command})
  test          Run unit tests
  isort         Run isort recursively from your current directory
  coverage      Run unit tests and check the coverage
```
