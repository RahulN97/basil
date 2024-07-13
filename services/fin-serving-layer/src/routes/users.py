from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from dependencies import DbClient
from models.user import User, UserCreate, UserDelete, UserGet, UserUpdate
from routes.common import handle_exceptions


router: APIRouter = APIRouter()


@router.get("/", response_model=User)
@handle_exceptions
async def get_user(db_client: DbClient, request: UserGet) -> User:
    user: Optional[User] = db_client.get_user(request.user_id)
    if user is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Failed to fetch user with id: {request.user_id}, not found",
        )
    return user


@router.post("/", response_model=User)
@handle_exceptions
async def create_user(db_client: DbClient, request: UserCreate) -> User:
    existing_user: Optional[User] = db_client.get_user(request.user_id)
    if existing_user is not None:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=f"User with id: {request.user_id}, name: {request.name} already exists",
        )

    now: datetime = datetime.now()
    user: User = User(
        user_id=request.user_id,
        name=request.name,
        email=request.email,
        creation_time=now,
        update_time=now,
    )
    db_client.upsert_user(user)
    return user


@router.put("/", response_model=User)
@handle_exceptions
async def update_user(db_client: DbClient, request: UserUpdate) -> User:
    cur_user: Optional[User] = db_client.get_user(request.user_id)
    if cur_user is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Failed to update user with id: {request.user_id}, not found",
        )

    new_user: User = User(
        user_id=request.user_id,
        name=request.name or cur_user.name,
        email=request.name or cur_user.email,
        creation_time=cur_user.creation_time,
        update_time=datetime.now(),
    )
    db_client.upsert_user(new_user)
    return new_user


@router.delete("/")
@handle_exceptions
async def delete_user(db_client: DbClient, request: UserDelete) -> None:
    return db_client.delete_user(request.user_id)
