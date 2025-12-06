#!/bin/bash
gunicorn langraph_tool:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
