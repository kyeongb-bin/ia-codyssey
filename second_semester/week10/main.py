import csv
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI, HTTPException

from model import TodoCreate, TodoItem

DATA_FILE = Path(__file__).parent / 'todos.csv'
FIELDNAMES = ['id', 'title', 'description', 'is_done']

app = FastAPI()


def initialize_storage() -> None:
    if not DATA_FILE.exists():
        DATA_FILE.write_text('id,title,description,is_done\n', encoding='utf-8')


def read_todos() -> List[Dict]:
    initialize_storage()
    todos: List[Dict] = []
    with DATA_FILE.open('r', encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            todos.append(
                {
                    'id': int(row['id']),
                    'title': row['title'],
                    'description': row['description'],
                    'is_done': row['is_done'].lower() == 'true',
                },
            )
    return todos


def write_todos(todos: List[Dict]) -> None:
    with DATA_FILE.open('w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        for todo in todos:
            writer.writerow(
                {
                    'id': todo['id'],
                    'title': todo['title'],
                    'description': todo['description'],
                    'is_done': str(todo['is_done']),
                },
            )


def generate_new_id(todos: List[Dict]) -> int:
    if not todos:
        return 1
    return max(todo['id'] for todo in todos) + 1


@app.get('/todos')
async def get_todos() -> List[Dict]:
    return read_todos()


@app.post('/todos', status_code=201)
async def create_todo(item: TodoCreate) -> Dict:
    todos = read_todos()
    new_todo = {
        'id': generate_new_id(todos),
        'title': item.title,
        'description': item.description,
        'is_done': item.is_done,
    }
    todos.append(new_todo)
    write_todos(todos)
    return new_todo


@app.get('/todos/{todo_id}')
async def get_single_todo(todo_id: int) -> Dict:
    todos = read_todos()
    for todo in todos:
        if todo['id'] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail='Todo not found')


@app.put('/todos/{todo_id}')
async def update_todo(todo_id: int, item: TodoItem) -> Dict:
    todos = read_todos()
    for index, todo in enumerate(todos):
        if todo['id'] == todo_id:
            updated_todo = todo.copy()
            if item.title is not None:
                updated_todo['title'] = item.title
            if item.description is not None:
                updated_todo['description'] = item.description
            if item.is_done is not None:
                updated_todo['is_done'] = item.is_done
            todos[index] = updated_todo
            write_todos(todos)
            return updated_todo
    raise HTTPException(status_code=404, detail='Todo not found')


@app.delete('/todos/{todo_id}')
async def delete_single_todo(todo_id: int) -> Dict:
    todos = read_todos()
    for index, todo in enumerate(todos):
        if todo['id'] == todo_id:
            deleted = todos.pop(index)
            write_todos(todos)
            return {'message': 'Todo deleted', 'todo': deleted}
    raise HTTPException(status_code=404, detail='Todo not found')


initialize_storage()

