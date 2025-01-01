from fastapi import FastAPI, HTTPException, Depends, Query
from models import Task, TaskCreate

app = FastAPI()

# dummy data source for persistence
db = []

def get_db():
    return db

@app.get("/")
async def root():
    return {"message": "Welcome to the To-Do API"}

@app.post("/tasks/", status_code=201)
async def create_task(task_data: TaskCreate, db: list = Depends(get_db)):
    task_id = len(db) + 1
    task = Task(id=task_id, **task_data.dict())
    db.append(task)
    return task

# read all tasks
@app.get("/tasks")
async def get_tasks(db: list = Depends(get_db)):
    return db

@app.get("/tasks/{task_id}")
async def get_task(task_id: int, db: list = Depends(get_db)):
    for task in db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail='Task not found.')

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, updated_data: TaskCreate, db: list = Depends(get_db)):
    for index, task in enumerate(db):
        if task.id == task_id:
            updated_task_data = updated_data.dict(exclude_unset=True)
            for key, value in updated_data.dict(exclude_unset=True).items():
                setattr(task, key, value)
            db[index] = task
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.patch("/tasks/{task_id}/toggle-complete", response_model=Task)
async def toggle_task_completion(task_id: int, db: list = Depends(get_db)):
    for task in db:
        if task.id == task_id:
            # Toggle the completion status
            task.completed = not task.completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")

from fastapi import FastAPI, HTTPException, Depends, Query

@app.patch("/tasks/mark-all-completeness")
async def mark_all_tasks_completeness(is_complete: bool = Query(...), db: list = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=404, detail="No tasks available.")

    # Update all tasks' completion status
    for task in db:
        task.completed = is_complete

    # Create a status message
    status = "Complete" if is_complete else "Incomplete"
    return {"message": f"All tasks marked as {status}"}



@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: list = Depends(get_db)):
    for index, task in enumerate(db):
        if task.id == task_id:
            db.pop(index)
            return {"message": "Task deleted successfully"}

    return HTTPException(status_code=404, detail='Task not found.')



