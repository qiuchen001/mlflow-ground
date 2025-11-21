from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MLFLOW_TRACKING_URI = "http://127.0.0.1:5002"

@app.get("/")
async def root():
    return {"message": "MLflow Custom UI Backend"}

@app.get("/experiments")
async def list_experiments():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{MLFLOW_TRACKING_URI}/api/2.0/mlflow/experiments/search?max_results=1000")
        return response.json()

@app.get("/experiments/{experiment_id}/runs")
async def list_runs(experiment_id: str):
    async with httpx.AsyncClient() as client:
        # MLflow search_runs is a POST request usually, but let's check docs.
        # Actually search_runs is POST /api/2.0/mlflow/runs/search
        response = await client.post(
            f"{MLFLOW_TRACKING_URI}/api/2.0/mlflow/runs/search",
            json={"experiment_ids": [experiment_id]}
        )
        return response.json()

@app.get("/runs/{run_id}")
async def get_run(run_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{MLFLOW_TRACKING_URI}/api/2.0/mlflow/runs/get?run_id={run_id}")
        return response.json()

@app.get("/runs/{run_id}/metrics/history")
async def get_metric_history(run_id: str, metric_key: str):
    async with httpx.AsyncClient() as client:
        params = {
            "run_id": run_id,
            "metric_key": metric_key,
            "max_results": 1000
        }
        response = await client.get(f"{MLFLOW_TRACKING_URI}/api/2.0/mlflow/metrics/get-history", params=params)
        return response.json()

@app.get("/runs/{run_id}/artifacts")
async def list_artifacts(run_id: str, path: str = None):
    async with httpx.AsyncClient() as client:
        params = {"run_id": run_id}
        if path:
            params["path"] = path
        response = await client.get(f"{MLFLOW_TRACKING_URI}/api/2.0/mlflow/artifacts/list", params=params)
        return response.json()

from fastapi.responses import Response

@app.get("/runs/{run_id}/artifacts/content")
async def get_artifact_content(run_id: str, path: str):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        params = {"run_id": run_id, "path": path}
        response = await client.get(f"{MLFLOW_TRACKING_URI}/get-artifact", params=params)
        
        # Check content type or extension to determine if it's an image
        content_type = response.headers.get("content-type", "")
        if "image" in content_type or path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
             return Response(content=response.content, media_type=content_type or "image/png")
        
        # For other types (assumed text), return raw content as text/plain to avoid JSON encoding
        return Response(content=response.content, media_type="text/plain")
