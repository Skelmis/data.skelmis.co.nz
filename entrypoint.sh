#!/usr/bin/env bash

uvicorn app:app --proxy-headers --host 0.0.0.0 --port 2200 --log-config=log_conf.yaml