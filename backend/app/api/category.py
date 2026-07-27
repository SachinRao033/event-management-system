from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category import (
    create_category,
    delete_category,
    get_all_categories,
    get_category,
    update_category,
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_category(
        db=db,
        category_create=category,
    )


@router.get(
    "/",
    response_model=List[CategoryResponse],
)
def read_all_categories(
    db: Session = Depends(get_db),
):
    return get_all_categories(db)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def read_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    return get_category(
        db=db,
        category_id=category_id,
    )


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_existing_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_category(
        db=db,
        category_id=category_id,
        category_update=category_update,
    )


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_category(
        db=db,
        category_id=category_id,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)