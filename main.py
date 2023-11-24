from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY

app = FastAPI()

# Example Histogram metric
request_duration_seconds = Histogram("myapp_request_duration_seconds", "Request duration in seconds")
requests_total = Counter("myapp_requests_total", "Total number of requests")

@app.get("/")
async def read_root():
    requests_total.inc()
    # Record the duration of this request in the Histogram metric
    with request_duration_seconds.time():
        # Your FastAPI application logic here
        return {"Hello": "World"}
    

@app.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    # Expose the metrics for Prometheus to scrape
    return PlainTextResponse(content=generate_latest(REGISTRY), status_code=200)

