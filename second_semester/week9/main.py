from fastapi import FastAPI
from todo import router as todo_router

app = FastAPI()

app.include_router(todo_router)

