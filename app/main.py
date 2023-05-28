import asyncio
from fastapi import FastAPI

from app.routers import todos_v1, todos_v2, todos_v3
from app.db import get_pool, get_async_pool

app = FastAPI()

pool = get_pool()
async_pool = get_async_pool()

app.include_router(todos_v1.router)
app.include_router(todos_v2.router)
app.include_router(todos_v3.router)


async def check_connections():
    while True:
        await asyncio.sleep(600)
        print("check connections")
        pool.check()


async def check_async_connections():
    while True:
        await asyncio.sleep(600)
        print("check async connections")
        await async_pool.check()


@app.on_event("startup")
def startup():
    asyncio.create_task(check_connections())
    asyncio.create_task(check_async_connections())


@app.get("/")
def read_root():
    return {"Hello": "World"}
