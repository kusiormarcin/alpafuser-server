# AlpaFuser Server - W.I.P.

## Description

Since [diffusers](https://apps.apple.com/us/app/diffusers/id1666309574) app on macOS is currently broken I decided to create a simple server that enables you to run diffusions.

This is a simple server created with Flask to provide a REST API to run diffusions.

In the next steps, I'll simplifying it even more.

I'll create frontend for this app (hopefully *soon*).

## Disclaimer

**This is a work in progress and not production ready!**

## Installation and running

Prerequisites:
- Mac with M chip - tested on M2 Max with 64GB of memory
- Python 3.12 or higher (not tested on any previous version at this point)
- Redis server

Copy .env.example to .env and fill in the necessary values.

`DIFFUSION_MODEL` - here you should provide a *huggingface* model name (see [here](https://huggingface.co/models?pipeline_tag=text-to-image&sort=downloads))

```shell
APP_URL="http://127.0.0.1:5000"
SCRIPT_PATH="ABSOLUTE_PATH_TO_THIS_DIRECTORY/generate.sh"
REDIS_URL="redis://localhost"
DIFFUSION_MODEL="stabilityai/stable-diffusion-xl-base-1.0"
```

In one terminal run:

```shell
$ python3 -m venv .venv
$ . ./.venv/bin/activate
$ pip install -r requirements.txt && pip install -e .
$ celery -A make_celery worker --loglevel INFO
```

In another terminal run:

```shell
$ . ./.venv/bin/activate
$ flask -A app run --debug
```

## Usage

App is running on the port `5000`.

Endpoints provided with the app:

- `POST` `/generate` - runs diffusions using [diffusers](https://github.com/huggingface/diffusers) library.

    Example request:

    ```json
    {
        "prompt": "Alpaca hiding in the bushes"
    }
    ```

    Example response:

    ```json
    {
        "request": {
            "prompt": "Alpaca hiding in the bushes"
        },
        "result_id": "0a08d415-ed90-4b81-bca5-2e9caa21ce82"
    }
    ```

- `GET` `/status/:id` - returns status of the job with id `:id`.

    
    Example response:

    ```json
    {
        "ready": true,
        "succesful": true,
        "value": "127.0.0.1:5000/output/0a08d415-ed90-4b81-bca5-2e9caa21ce82.jpg"
    }
    ```