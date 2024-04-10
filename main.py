from fastapi import FastAPI
import threading
import requests

url = 'http://nestio.space/api/satellite/data'

app = FastAPI()
cache = []


def set_interval(func, seconds):
    def helper():
        set_interval(func, seconds)
        func()

    thread = threading.Timer(seconds, helper)
    thread.start()
    return thread


def cache_builder(object):
    cache.append(object)


def poll():
    r = requests.get(url)
    print(r.json())
    cache_builder(r.json())


set_interval(poll, 5)


@app.get("/api/stats")
async def stats():
    return cache


@app.get("/api/health/")
async def health(name):
    return {"message": f"Hello {name}"}
