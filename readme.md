### prerequisites:
- running redis instance available at localhost: 6379
- create python virtualenv
- `pip install -r requirements.txt`
- `python manage.py migrate`

### how to run test script
- `mprof run daphne -b 0.0.0.0 -p=8087 djws.asgi:application`
- OR `mprof run --multiprocess gunicorn djws.asgi:application -b :8087 -w 2 -k uvicorn.workers.UvicornWorker`
- `python scripts/ws_test.py`
- stop server (daphne OR gunicorn+uvicorn)
- `mprof plot`
