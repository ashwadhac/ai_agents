from langchain_core.tools import tool

from database import SessionLocal
from models import Todo


@tool
def add_todo(task: str) -> str:
    """Add a new todo task to the database."""

    db = SessionLocal()

    try:
        todo = Todo(task=task)

        db.add(todo)
        db.commit()
        db.refresh(todo)

        return f"Todo added successfully. ID: {todo.id}, Task: {todo.task}"

    finally:
        db.close()


@tool
def get_todos() -> str:
    """Get all todo tasks from the database."""

    db = SessionLocal()

    try:
        todos = db.query(Todo).all()

        if not todos:
            return "No todos found."

        result = []

        for todo in todos:
            status = "Completed" if todo.completed else "Pending"

            result.append(
                f"ID: {todo.id} | Task: {todo.task} | Status: {status}"
            )

        return "\n".join(result)

    finally:
        db.close()


@tool
def complete_todo(todo_id: int) -> str:
    """Mark a todo as completed using its ID."""

    db = SessionLocal()

    try:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()

        if not todo:
            return f"Todo with ID {todo_id} not found."

        todo.completed = True

        db.commit()

        return f"Todo {todo_id} marked as completed."

    finally:
        db.close()


@tool
def delete_todo(todo_id: int) -> str:
    """Delete a todo using its ID."""

    db = SessionLocal()

    try:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()

        if not todo:
            return f"Todo with ID {todo_id} not found."

        db.delete(todo)
        db.commit()

        return f"Todo {todo_id} deleted successfully."

    finally:
        db.close()