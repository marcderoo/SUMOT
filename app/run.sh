#/bin/bash

python3 app.py
uvicorn app.api:app --host "0.0.0.0"