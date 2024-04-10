from fastapi import FastAPI
import threading
import requests

url = 'http://nestio.space/api/satellite/data'

app = FastAPI()
cache = {}
def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def cache_builder(object):
    cache

def poll():
    r = requests.get(url)
    print(r.json())

set_interval(poll, 5)


@app.get("api/stats")
async def stats():
    return {"message": "Hello World"}


@app.get("api/health/")
async def health(name):
    return {"message": f"Hello {name}"}