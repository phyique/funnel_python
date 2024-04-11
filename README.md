# Funnel Leasing Coding Assignment

This repo is the funnel short app

# Getting started

To get the Python server running locally:

- Clone this repo
- `pip install -r requirements` to install all required dependencies
- `uvicorn main:app --reload` to start the local server

# Code Overview

## Dependencies

- [fastapi](https://github.com/tiangolo/fastapi) - FastAPI framework, high performance, easy to learn, fast to code, ready for production
- [requests](https://github.com/request/request) - Simplified HTTP request client.
- ...to be continued


## Application Structure

- `main.py` - The entry point to our application. This file defines our fastapi server and performs background polling logic for satellite api

# REST API

The REST API to the example app is described below.

### Request

`GET /api/stats`

    curl --location --request GET 'http://localhost:8000/api/stats'

### Response

    {
        "data": {
            "minimum": null,
            "maximum": null,
            "average": 0
        }
    }

### Request

`GET /api/health`

    curl --location --request GET 'http://localhost:8000/api/health' 

### Response
    {
        "data": {
            "message": "Sustained Low Earth Orbit Resumed",
            "average": 171.16908827883267
        }
    }
