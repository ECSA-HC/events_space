import math
from sqlalchemy import or_
from starlette import status
from typing import Annotated
from sqlalchemy.orm import Session
from core.database import get_db
from models.models import OrgUnit
from schemas.events_space import OrgUnitSchema
from dependencies.auth_dependency import Auth
from dependencies.dependency import Dependency
from dependencies.auth_dependency import get_current_user
from fastapi import APIRouter, HTTPException, Depends, Query, Request

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


def get_dependency(db: Session = Depends(get_db)) -> Dependency:
    return Dependency(db)


def get_auth_dependency(db: Session = Depends(get_db)) -> Auth:
    return Auth(db)


def get_object(id, db, model):
    data = db.query(model).filter(model.id == id).first()
    if data is None:
        raise HTTPException(
            status_code=404, detail=f"ID {id} : Does not exist")
    return data


@router.get("/")
async def get_org_units(
    request: Request,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = 10,
    search: str = "",
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
        
    auth_dependency.secure_access("VIEW_ORG_UNIT", current_user['user_id'])
    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        current_user['user_id'],
        'VIEW_ORG_UNITS',
        current_user['username'],
        client_ip,
        "Get all org units"
    )

    search_filter = or_(
        OrgUnit.name.ilike(f"%{search}%"),
    )

    org_unit_query = db.query(OrgUnit).filter(
        search_filter, OrgUnit.deleted_at == None)

    total_count = org_unit_query.count()
    org_units = org_unit_query.offset(skip).limit(limit).all()

    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": org_units}



@router.post("/")
async def add_org_unit(
    request: Request,
    org_unit_schema: OrgUnitSchema,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    auth_dependency.secure_access("ADD_ORG_UNIT", current_user['user_id'])
    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        current_user['user_id'],
        'ADD_ORG_UNIT',
        current_user['username'],
        client_ip,
        org_unit_schema.name
    )

    create_org_unit_model = OrgUnit(
        name=org_unit_schema.name,
        type=org_unit_schema.type,
        description=org_unit_schema.description,
    )

    db.add(create_org_unit_model)
    db.commit()
    return org_unit_schema


@router.get("/{org_unit_id}")
async def get_org_unit(
    request: Request,
    org_unit_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    auth_dependency.secure_access("VIEW_ORG_UNIT", current_user['user_id'])
    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        current_user['user_id'],
        'VIEW_ORG_UNIT',
        current_user['username'],
        client_ip,
        f"View org unit id {org_unit_id}"
    )
    return get_object(org_unit_id, db, OrgUnit)


@router.put("/{org_unit_id}")
async def update_org_unit(
    request: Request,
    org_unit_id: int,
    current_user: user_dependency,
    org_unit_schema: OrgUnitSchema,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    auth_dependency.secure_access("UPDATE_ORG_UNIT", current_user['user_id'])
    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        current_user['user_id'],
        'UPDATE_ORG_UNIT',
        current_user['username'],
        client_ip,
        f"Update orgvunit id {org_unit_id} org unit code {org_unit_schema.name}"
    )

    org_unit_model = get_object(org_unit_id, db, OrgUnit)

    org_unit_model.name = org_unit_schema.name
    org_unit_model.type = org_unit_schema.type
    org_unit_model.description = org_unit_schema.description

    db.commit()
    db.refresh(org_unit_model)
    return org_unit_schema


@router.delete("/{org_unit_id}")
async def delete_org_unit(
    request: Request,
    org_unit_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    auth_dependency.secure_access("DELETE_ORG_UNIT", current_user['user_id'])
    org_unit = get_object(org_unit_id, db, OrgUnit)

    try:
        db.delete(org_unit)
        db.commit()
    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete org unit") from error

    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        current_user['user_id'],
        'DELETE_ORG_UNIT',
        current_user['username'],
        client_ip,
        f"Update org_unit id {org_unit_id}, org_unit {org_unit.name} "
    )
    return {"detail": "Org Unit successfully deleted"}
