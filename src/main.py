import json
from typing import Any, Dict

from bson.objectid import ObjectId
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient

from constants import DATABASE_HOST, TITLE

# Set up the MongoDB client and database
client = MongoClient(DATABASE_HOST)
db = client.database
collection = db.configs

app = FastAPI(title=TITLE)


@app.get("/config")
def get_configs() -> Any:
    configs = collection.find()
    return json.loads(json.dumps([{"id": str(config["_id"]), "data": config} for config in configs], default=str))


@app.get("/config/{id}")
def get_config(id: str) -> Any:
    config = collection.find_one({"_id": ObjectId(id)})
    if not config:
        raise HTTPException(status_code=404, detail="Config not found")
    return json.loads(json.dumps({"id": str(config["_id"]), "data": config}, default=str))


@app.put("/config/{id}")
def set_config(id: str, payload: Dict[str, Any]) -> Any:
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": payload})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Config not found")
    return "Success"


@app.post("/config")
def insert_config(payload: Dict[str, Any]) -> Any:
    result = collection.insert_one(payload)
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to insert config")
    return "Success"


@app.get("/health")
def get_health() -> Any:
    try:
        client.admin.command("ping")
        return "Success"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)