import requests

url = "http://127.0.0.1:5002/api/2.0/mlflow/metrics/get-history"
params = {
    "run_id": "a56e5979406e449292cb4f8a141b2d95",
    "metric_key": "train/loss",
    "max_results": 1000
}

try:
    response = requests.get(url, params=params)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
