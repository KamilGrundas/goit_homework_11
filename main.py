from src.routes import contacts, auth, users
import redis.asyncio as redis
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

app = FastAPI()

origins = [
    "http://localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix='/api')

@app.on_event("startup")
async def startup():
    """
    Performs startup event tasks. Initializes the Redis connection and FastAPI Limiter for rate limiting.

    This function is called when the FastAPI application starts, setting up the necessary components
    for rate limiting by connecting to a Redis database.
    """
    r = await redis.Redis(host='localhost', port=6379, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)

@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def index():
    """
    A simple index route to demonstrate rate limiting.

    This route is rate limited to 2 requests every 5 seconds per client. It's a basic example to show how
    rate limiting works in a FastAPI application using FastAPILimiter.

    :return: A greeting message.
    :rtype: dict
    """
    return {"msg": "Hello World"}

# Entry point for running the application.
# This allows the application to be started using Uvicorn directly from the command line.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
