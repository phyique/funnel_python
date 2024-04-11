from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import threading
import requests

url = 'http://nestio.space/api/satellite/data'

app = FastAPI()
scheduler = BackgroundScheduler()
cache = []
sustained = False
thread = None


def set_interval(func, seconds):
    global thread

    def helper():
        set_interval(func, seconds)
        func()

    thread = threading.Timer(seconds, helper)
    thread.start()
    return thread


def satellite_time_lapse(variable):
    time_utc = datetime.now().utcnow()
    last_updated = datetime.fromisoformat(variable['last_updated'])
    variable['time_lapse'] = (time_utc - last_updated).seconds / 60
    return variable


def cache_builder(obj):
    global cache
    cache.append(obj)
    cache = list(map(satellite_time_lapse, cache))
    cache = list(filter(lambda n: n['time_lapse'] < 5, cache))
    print(cache)


def poll():
    r = requests.get(url)
    cache_builder(r.json())


def is_sustained(average):
    global sustained
    sustained = average > 160


# poll for satellite date every 5 seconds
# set_interval(poll, 5)

@app.on_event("startup")
def start_background_processes():
    scheduler.add_job(poll, "interval", seconds=5)
    scheduler.start()

@app.get("/api/stats")
async def stats():
    altitudes = list(map(lambda n: n['altitude'], cache))
    return {'data': {'maximum': max(altitudes),
                     'minimum': min(altitudes),
                     'average': sum(altitudes) / len(altitudes)}}


@app.get("/api/health/")
async def health():
    global sustained
    message = 'Altitude is A-OK'
    a_min_cache = list(filter(lambda n: n['time_lapse'] < 1, cache))
    altitudes = list(map(lambda n: n['altitude'], a_min_cache))
    average = sum(altitudes) / (1 if len(altitudes) == 0 else len(altitudes))
    if average < 160:
        message = 'WARNING: RAPID ORBITAL DECAY IMMINENT'
    if average >= 160 and not sustained:
        message = 'Sustained Low Earth Orbit Resumed'
    # set_interval(is_sustained(average), 60)
    return {'data': {'message': message,
                     'average': average}}
