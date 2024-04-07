#!/bin/bash
python -m ems.composites.alembic_runner upgrade head
uvicorn --app-dir src ems.composites.http_api:app --host 0.0.0.0 --port 3000
