from typing import Any

from fastapi import FastAPI
from constants import TITLE

app = FastAPI(
    title=TITLE
)


@app.get("/config/{id}")
def get_config(id: int) -> Any:
    return {
        "id": 1,
        "test": "config"
    }


@app.put("/config/{id}")
def set_config(id: int, payload: Any) -> Any:
    return "Success"


@app.get("/health")
def get_health(id: int, payload: Any) -> Any:
    return "Success"
