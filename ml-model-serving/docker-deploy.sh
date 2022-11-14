#!/bin/env bash

docker build -t sklearn-fastapi .
docker run -d -p 8000:80 sklearn-fastapi
