import json
import pprint

from fastapi import FastAPI, Request, Response


configs_cache = {}


def cache_configs():
    with open("configs.json", "r") as fp:
        mock_configs = json.load(fp)
        for config in mock_configs["configs"]:
            url_path = config["url_path"]
            http_method = config["http_method"].upper()

            if configs_cache.get(url_path) is None:
                configs_cache[url_path] = {}

            configs_cache[url_path][http_method] = config

    pprint.pprint(configs_cache)


app = FastAPI(on_startup=[cache_configs])


@app.get("/health-check")
def health():
    return {"status": "OK"}


@app.middleware("http")
async def interceptor(request: Request, call_next):
    url_path = request.scope["path"]
    http_method = request.scope["method"]

    print(f"interceptor: url_path: {url_path}, http_method: {http_method}")

    if url_path in configs_cache:
        mock_config = configs_cache[url_path][http_method]

        response = Response(
            content=json.dumps(mock_config["response_body"]),
            status_code=mock_config["status_code"],
        )
    else:
        response = await call_next(request)

    return response
