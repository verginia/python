from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.models import Todo
from src.schemas.todo_schemas import TodoCreate, Todo as TodoSchema

router = APIRouter(prefix="/todo", tags=["todo"])

@router.post("/", response_model=TodoSchema)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.title == todo.title).first()
    if db_todo:
        raise HTTPException(status_code=400, detail="Todo already created")

    db_todo = Todo(
        title = todo.title,
        description=todo.description,
        completed=todo.completed,
        user_id=todo.user_id
    )

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get("/", response_model=List[TodoSchema])
def get_todos(db: Session = Depends(get_db)):
    """Get all todos"""
    return db.query(Todo).all()

@router.get("/{todo_id}", response_model=TodoSchema)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """Get a specific to do by ID"""
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.put("/{todo_id}", response_model=TodoSchema)
def update_todo(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    """Update a to do by ID"""
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    for field, value in todo.dict().items():
        setattr(db_todo, field, value)

    db.commit()
    db.refresh(db_todo)
    return db_todo
@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a to do by ID"""
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted successfully"}
