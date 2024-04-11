from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import requests

url = 'http://nestio.space/api/satellite/data'

app = FastAPI()
scheduler = BackgroundScheduler()
cache = []
sustained = False


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
    print("is_sustained_called", average)
    sustained = average > 130


@app.on_event("startup")
def start_background_processes():
    scheduler.add_job(poll, "interval", seconds=5)
    scheduler.start()


@app.get("/api/stats")
async def stats():
    altitudes = list(map(lambda n: n['altitude'], cache))
    if len(altitudes) == 0:
        altitudes = [1]
    return {'data': {'maximum': max(altitudes),
                     'minimum': min(altitudes),
                     'average': sum(altitudes) / len(altitudes)}}


@app.get("/api/health")
async def health():
    global sustained
    a_min_cache = list(filter(lambda n: n['time_lapse'] < 1, cache))
    altitudes = list(map(lambda n: n['altitude'], a_min_cache))
    average = sum(altitudes) / (1 if len(altitudes) == 0 else len(altitudes))
    if average < 160:
        message = 'WARNING: RAPID ORBITAL DECAY IMMINENT'
    elif average >= 160 and not sustained:
        message = 'Sustained Low Earth Orbit Resumed'
    else:
        message = 'Altitude is A-OK'
    scheduler.add_job(is_sustained, 'date', run_date=datetime.now() + timedelta(seconds=60), args=[average])
    return {'data': {'message': message,
                     'average': average}}
