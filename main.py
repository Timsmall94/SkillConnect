# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import Database
import sqlite3
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Connect to SQLite3 
database = Database(DATABASE_URL)


# Define models
class Worker(BaseModel):
    name: str
    phone_number: str
    location: str
    address: str
    skilled_sector: str


# SQLite3 specific functions
def create_table():
    with sqlite3.connect("test.db") as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS workers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            location TEXT NOT NULL,
            address TEXT NOT NULL,
            skilled_sector TEXT NOT NULL
            )"""
        )


async def insert_worker(worker: Worker):
    query = """INSERT INTO workers (name, phone_number, location, address, skilled_sector)
               VALUES (:name, :phone_number, :location, :address, :skilled_sector)"""
    await database.execute(query=query, values=worker.dict())


async def get_worker(worker_id: int):
    query = "SELECT * FROM workers WHERE id = :id"
    return await database.fetch_one(query=query, values={"id": worker_id})


async def get_all_workers():
    query = "SELECT * FROM workers"
    return await database.fetch_all(query=query)


# Routes
@app.post("/workers/")
async def create_worker(worker: Worker):
    await insert_worker(worker)
    return {"message": "Worker created successfully"}


@app.get("/workers/{worker_id}/")
async def read_worker(worker_id: int):
    worker = await get_worker(worker_id)
    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker


@app.get("/workers/")
async def read_all_workers():
    workers = await get_all_workers()
    return workers
