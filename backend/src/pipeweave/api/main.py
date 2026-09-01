"""FastAPI Main"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="PipeWeave Platform API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def root(): return {"service": "PipeWeave Engine", "version": "1.0.0", "status": "HEALTHY"}

@app.get("/api/pipelines")
async def list_pipelines(): return [{"id": "pipe-ecom", "name": "E-Commerce Stream", "nodes_count": 5}]

@app.get("/api/runs")
async def list_runs(): return [{"run_id": "run-01", "state": "SUCCESS", "records_processed": 50000}]

@app.get("/api/telemetry/metrics")
async def get_metrics(): return {"throughput_rps": 14500.0, "latency_p95_ms": 24.1}
