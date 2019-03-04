# ![Marvin](https://user-images.githubusercontent.com/5514990/53703935-bc0cc900-3e49-11e9-9d9e-952101a4c0cf.png) Marvin

> Marvin, more fully known as Marvin the *Paranoid Android*, is an incredibly brilliant but overwhelmingly depressed robot manufactured by the **Sirius Cybernetics Corporation** and unwilling servant to the crew of the *Heart of Gold*.

## No seriously, what is Marvin?

Marvin is a **Slack Bot layout** for *Flask* to develop *Slack* event handlers and deploy on *AWS Lambda* + *API Gateway*.

## Quickstart

Install [AWS Command Line Interface](https://docs.aws.amazon.com/es_es/cli/latest/userguide/cli-chap-install.html) and configure the *marvin* profile

```sh
$ pip install awscli --upgrade --user
$ aws configure --profile marvin
```

Then create a zappa configuration file `zappa_settings.json` and upload your `config.json` file to your s3 bucket using the same url as the `remote_env` field from your `zappa_settings.json`.

Here we go!

```sh
$ make lambda
$ make zappa cmd=deploy
```

## Commands

```sh
$ make help
```

```
Please use 'make <target>' where <target> is one of
  build         Build docker image
  up            Run docker container and build if the image does not exist
  restart       Restart docker container
  rm            Remove docker container
  logs          View output from docker container
  sh            Run bash shell on the container
  run           Run a local development server
  requirements  Install pip requirements from $REQUIREMENTS_FILES variable
  lambda        Build λ docker container
  zappa         Run zappa command (usage: make zappa cmd={command})
  test          Run unit tests
  isort         Run isort recursively from your current directory
  coverage      Run unit tests and check the coverage
```
