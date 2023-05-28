from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from psycopg.rows import class_row

from app.db import get_conn

router = APIRouter(prefix="/v1/todos")


class ToDo(BaseModel):
    id: int | None
    name: str
    completed: bool


@router.post("")
def create_todo(todo: ToDo):
    with get_conn() as conn:
        conn.execute(
            "insert into todos (name, completed) values (%s, %s)",
            [todo.name, todo.completed],
        )


@router.get("")
def get_todos():
    with get_conn() as conn, conn.cursor(row_factory=class_row(ToDo)) as cur:
        records = cur.execute("select * from todos").fetchall()
        return records


@router.get("/{id}")
def get_todo(id: int):
    with get_conn() as conn, conn.cursor(row_factory=class_row(ToDo)) as cur:
        record = cur.execute("select * from todos where id=%s", [id]).fetchone()
        if not record:
            raise HTTPException(404)
        return record


@router.put("/{id}")
def update_todo(id: int, todo: ToDo):
    with get_conn() as conn, conn.cursor(row_factory=class_row(ToDo)) as cur:
        record = cur.execute(
            "update todos set name=%s, completed=%s where id=%s returning *",
            [todo.name, todo.completed, id],
        ).fetchone()
        return record


@router.delete("/{id}")
def delete_todo(id: int):
    with get_conn() as conn:
        conn.execute("delete from todos where id=%s", [id])
