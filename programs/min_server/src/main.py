import json
import logging
import pprint
from datetime import datetime
from fastapi import FastAPI, Request


app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time: datetime = datetime.now()
    response = await call_next(request)
    process_time = datetime.now() - start_time

    response.headers["X-Process-Time"] = str(process_time.total_seconds())
    logging.info(pprint.pformat(request.scope))

    return response


@app.get("/sample")
async def sample_get(request: Request):
    logging.info("Entered")

    headers = dict(request.headers)
    query_params = dict(request.query_params)

    return {
        "method": request.method,
        "query_params": query_params,
        "headers": headers,
        "client": {
            "host": request.client.host,
            "port": request.client.port,
        },
    }


@app.post("/sample")
async def sample_post(request: Request):
    logging.info("Entered")

    headers = dict(request.headers)
    query_params = dict(request.query_params)
    body = await request.json()

    return {
        "method": request.method,
        "query_params": query_params,
        "headers": headers,
        "body": body,
        "client": {
            "host": request.client.host,
            "port": request.client.port,
        },
    }


@app.api_route(
    "/sample-any", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]
)
async def sample_any(request: Request):
    logging.info("Entered")

    headers = dict(request.headers)
    query_params = dict(request.query_params)

    # body = await request.json() if request.method in ["POST", "PUT", "PATCH"] else None
    body = await request.body()

    # Try to parse the body as JSON, if possible
    try:
        body = json.loads(body)
    except json.JSONDecodeError:
        body = body.decode()  # fallback to raw body as string

    return {
        "method": request.method,
        "query_params": query_params,
        "headers": headers,
        "body": body,
        "client": {
            "host": request.client.host,
            "port": request.client.port,
        },
    }


def init_logging() -> None:
    logging.Formatter.formatTime = (
        lambda self, record, datefmt=None: datetime.fromtimestamp(record.created)
        .astimezone()
        .isoformat(timespec="microseconds")
    )

    logging.basicConfig(
        format="%(asctime)s | %(levelname)-8s | %(module)s:%(funcName)s:%(lineno)d: %(message)s",
        level=logging.INFO,
        # handlers=[
        #     logging.StreamHandler(),
        #     logging.FileHandler("out.txt"),
        # ],
    )


init_logging()
