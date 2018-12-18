import uvicorn

from djws.asgi import application

if __name__ == "__main__":
    uvicorn.run(application, "127.0.0.1", 8089, log_level="debug")
