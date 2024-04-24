from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import requests
import time

url = 'http://nestio.space/api/satellite/data'

scheduler = BackgroundScheduler()
cache = []
sustained = False


@asynccontextmanager
async def lifespan(_: FastAPI):
    scheduler.add_job(poll, 'interval', seconds=5, max_instances=3)
    scheduler.start()
    yield
    scheduler.shutdown()
    print('clean up lifespan')

app = FastAPI(lifespan=lifespan)


@app.middleware('http')
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response


def time_elapsed(variable):
    time_utc = datetime.now().utcnow()
    last_updated = datetime.fromisoformat(variable['last_updated'])
    variable['time_lapse'] = (time_utc - last_updated).seconds / 60
    return variable


def cache_builder(obj):
    global cache
    cache.append(obj)
    cache = list(map(time_elapsed, cache))
    cache = list(filter(lambda n: n['time_lapse'] < 5, cache))
    print(cache)


def poll():
    r = requests.get(url)
    cache_builder(r.json())


def set_sustained_status(status):
    global sustained
    sustained = status


@app.get('/api/stats')
async def stats():
    altitudes = list(map(lambda n: n['altitude'], cache))
    if len(altitudes) == 0:
        altitudes = [1]
    return {'data': {'maximum': max(altitudes),
                     'minimum': min(altitudes),
                     'average': sum(altitudes) / len(altitudes)}}


@app.get('/api/health')
async def health():
    global sustained
    a_min_cache = list(filter(lambda n: n['time_lapse'] < 1, cache))
    altitudes = list(map(lambda n: n['altitude'], a_min_cache))
    average = sum(altitudes) / (1 if len(altitudes) == 0 else len(altitudes))
    if average < 160:
        message = 'WARNING: RAPID ORBITAL DECAY IMMINENT'
        sustained = False
    elif average >= 160 and not sustained:
        message = 'Sustained Low Earth Orbit Resumed'
        scheduler.add_job(set_sustained_status, 'date', run_date=datetime.now() + timedelta(seconds=60), args=[True])
    else:
        message = 'Altitude is A-OK'
    return {'data': {'message': message,
                     'average': average}}
