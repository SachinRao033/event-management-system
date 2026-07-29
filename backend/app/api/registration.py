from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user

from app.models.user import User

from app.schemas.registration import (
    RegistrationCreate,
    RegistrationUpdate,
    RegistrationResponse,
)

from app.services.registration import (
    create_registration,
    get_registration,
    get_registrations_by_user,
    get_registrations_by_event,
    update_registration,
)

router = APIRouter(
    prefix="/registrations",
    tags=["Registrations"],
)


@router.post(
    "/",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_for_event(
    registration: RegistrationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_registration(
        db=db,
        registration_create=registration,
        user_id=current_user.id,
    )


@router.get(
    "/user/me",
    response_model=List[RegistrationResponse],
)
def get_my_registrations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_registrations_by_user(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/event/{event_id}",
    response_model=List[RegistrationResponse],
)
def get_event_registrations(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_registrations_by_event(
        db=db,
        event_id=event_id,
    )


@router.get(
    "/{event_id}",
    response_model=RegistrationResponse,
)
def get_my_registration(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_registration(
        db=db,
        user_id=current_user.id,
        event_id=event_id,
    )


@router.put(
    "/{event_id}",
    response_model=RegistrationResponse,
)
def update_my_registration(
    event_id: int,
    registration_update: RegistrationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_registration(
        db=db,
        user_id=current_user.id,
        event_id=event_id,
        registration_update=registration_update,
    )