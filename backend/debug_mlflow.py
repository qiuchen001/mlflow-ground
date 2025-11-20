import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri("http://127.0.0.1:5002")
client = MlflowClient()

run_id = "a56e5979406e449292cb4f8a141b2d95"
metric_key = "train/loss"

try:
    history = client.get_metric_history(run_id, metric_key)
    print(f"Found {len(history)} metrics for {metric_key}")
    for m in history[:5]:
        print(m)
except Exception as e:
    print(f"Error: {e}")
