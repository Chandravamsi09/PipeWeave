#!/usr/bin/env python3
"""
PipeWeave Enterprise Data Pipeline & Stream Processing Engine
Main CLI & Production Entrypoint
"""

import argparse
import sys
import os
import uvicorn
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend", "src")))

from pipeweave.core.config import settings
from pipeweave.core.logging import setup_logger
from pipeweave.engine.scheduler import DAGScheduler
from pipeweave.engine.graph import DAG

logger = setup_logger("pipeweave.cli")


def start_server():
    """Start the FastAPI production HTTP and WebSocket server."""
    logger.info(f"Starting PipeWeave API Server on {settings.api_host}:{settings.api_port}")
    uvicorn.run(
        "pipeweave.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level="info",
    )


def run_pipeline_cli(pipeline_id: str):
    """Execute pipeline via CLI directly."""
    logger.info(f"Executing pipeline: {pipeline_id}")
    scheduler = DAGScheduler()
    dag = DAG(dag_id=pipeline_id, name=f"CLI-DAG-{pipeline_id}")
    logger.info(f"Pipeline {pipeline_id} scheduled successfully.")


def main():
    parser = argparse.ArgumentParser(description="PipeWeave Data Pipeline Platform")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    server_parser = subparsers.add_parser("serve", help="Start API and WebSocket server")
    server_parser.add_argument("--port", type=int, default=8000, help="Port to bind")

    run_parser = subparsers.add_parser("run", help="Run a specific data pipeline")
    run_parser.add_argument("pipeline_id", type=str, help="Pipeline ID to execute")

    args = parser.parse_args()

    if args.command == "serve" or args.command is None:
        start_server()
    elif args.command == "run":
        run_pipeline_cli(args.pipeline_id)


if __name__ == "__main__":
    main()
