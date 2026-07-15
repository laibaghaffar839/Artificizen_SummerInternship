from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import Task, User
from app.schemas import TaskCreate, TaskResponse, TaskUpdate

from app.dependencies import get_current_user


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)



# Create Task


@router.post("/",response_model=TaskResponse,status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        due_date=task.due_date,
        owner_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task




# Get All Tasks


@router.get("/",response_model=list[TaskResponse])
def get_tasks(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    query = db.query(Task).filter(
        Task.owner_id == current_user.id
    )


    if status:
        query = query.filter(
            Task.status == status
        )


    return query.all()




# Get Single Task


@router.get("/{task_id}",response_model=TaskResponse)
def get_single_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()


    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


    return task




# Update Task


@router.put("/{task_id}",response_model=TaskResponse)
def update_task(
    task_id: int,
    updated_task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()


    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


    if updated_task.title:
        task.title = updated_task.title

    if updated_task.description:
        task.description = updated_task.description

    if updated_task.status:
        task.status = updated_task.status

    if updated_task.due_date:
        task.due_date = updated_task.due_date


    db.commit()
    db.refresh(task)


    return task




# Delete Task


@router.delete( "/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()


    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


    db.delete(task)
    db.commit()


    return {
        "message": "Task deleted successfully"
    }