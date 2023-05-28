from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from psycopg.rows import class_row

from app.db import get_async_pool

router = APIRouter(prefix="/v3/todos")

pool = get_async_pool()


class ToDo(BaseModel):
    id: int | None
    name: str
    completed: bool


@router.post("")
async def create_todo(todo: ToDo):
    async with pool.connection() as conn:
        await conn.execute(
            "insert into todos (name, completed) values (%s, %s)",
            [todo.name, todo.completed],
        )


@router.get("")
async def get_todos():
    async with pool.connection() as conn, conn.cursor(
        row_factory=class_row(ToDo)
    ) as cur:
        await cur.execute("select * from todos")
        records = await cur.fetchall()
        return records


@router.get("/{id}")
async def get_todo(id: int):
    async with pool.connection() as conn, conn.cursor(
        row_factory=class_row(ToDo)
    ) as cur:
        await cur.execute("select * from todos where id=%s", [id])
        record = await cur.fetchone()
        if not record:
            raise HTTPException(404)
        return record


@router.put("/{id}")
async def update_todo(id: int, todo: ToDo):
    async with pool.connection() as conn, conn.cursor(
        row_factory=class_row(ToDo)
    ) as cur:
        await cur.execute(
            "update todos set name=%s, completed=%s where id=%s returning *",
            [todo.name, todo.completed, id],
        )
        record = await cur.fetchone()
        return record


@router.delete("/{id}")
async def delete_todo(id: int):
    async with pool.connection() as conn:
        await conn.execute("delete from todos where id=%s", [id])
