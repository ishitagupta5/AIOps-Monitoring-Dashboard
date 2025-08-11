from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import random, time

app = Flask(__name__)

# Metrics (these are the numbers we track)
REQS = Counter("app_requests_total", "Total requests", ["endpoint"])
LAT = Histogram("app_request_latency_seconds", "Request latency", ["endpoint"],
                buckets=[0.05, 0.1, 0.2, 0.5, 1, 2, 5])
ANOMALY = Gauge("ai_anomaly_score", "Simulated anomaly score (0-1)")
INFER_MS = Gauge("ai_inference_latency_ms", "Simulated inference latency in ms")

@app.get("/healthz")
def health():
    return "ok", 200

@app.get("/predict")
def predict():
    start = time.time()
    latency = random.uniform(50, 300)   # pretend to take 50–300 ms
    time.sleep(latency / 1000.0)
    score = random.random()  # pretend AI gives a score between 0 and 1
    ANOMALY.set(score)
    INFER_MS.set(latency)
    REQS.labels("/predict").inc()
    LAT.labels("/predict").observe(time.time() - start)
    return jsonify({"anomaly_score": score, "inference_ms": latency})

@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
