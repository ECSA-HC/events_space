import math, os
import uuid
import shutil
from fastapi.responses import JSONResponse
from sqlalchemy import or_
from fastapi import status, HTTPException,File,Form,UploadFile
from typing import Annotated
from core.database import get_db
from sqlalchemy.orm import Session
import utils.mailer_util as mailer_util
from datetime import datetime, timedelta
from dependencies.auth_dependency import Auth
from dependencies.dependency import Dependency
from dependencies.auth_dependency import get_current_user
from fastapi import APIRouter, HTTPException, Depends, Query, Request
from models.models import Event, User, Registration, Document,Link
from schemas.events_space import EventSchema, RegistrationSchema, LinkSchema


router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]

def get_dependency(db: Session = Depends(get_db)) -> Dependency:
    return Dependency(db)

def get_auth_dependency(db: Session = Depends(get_db)) -> Auth:
    return Auth(db)

EVENT_DOCUMENT_DIR = "uploads/event/documents"
if not os.path.exists(EVENT_DOCUMENT_DIR):
    os.makedirs(EVENT_DOCUMENT_DIR)

def get_object(id: int, db: Session, model):
    data = db.query(model).filter(
        model.id == id,
        model.deleted_at.is_(None)
    ).first()
    if data is None:
        raise HTTPException(
            status_code=404,
            detail=f"{model.__name__} with ID {id} does not exist or has been deleted"
        )
    return data


@router.get("/")
async def get_events(
    request: Request,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    auth_dependency.secure_access("VIEW_EVENT", current_user['user_id'])
    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        current_user['user_id'],
        'VIEW_EVENTS',
        current_user['username'],
        client_ip,
        "Get all events"
    )

    search_filter = or_(
        Event.event.ilike(f"%{search}%"),
        Event.theme.ilike(f"%{search}%"),
        Event.description.ilike(f"%{search}%"),
    )  
      
    events_query = db.query(Event).filter(
        search_filter, Event.deleted_at == None)

    total_count = events_query.count()
    events = events_query.offset(
        (skip - 1) * limit).limit(limit).all()

    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": events}


@ router.post("/")
async def add_event(
    request: Request,
    event_schema: EventSchema,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    auth_dependency.secure_access("ADD_EVENT", current_user["user_id"])

    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        current_user['user_id'],
        'ADD_EVENT',
        current_user['username'],
        client_ip,
        event_schema.event
    )

    create_event_model = Event(
        org_unit_id=event_schema.org_unit_id,
        country_id=event_schema.country_id,
        user_id=current_user["user_id"],
        event=event_schema.event,
        theme=event_schema.theme,
        description=event_schema.description,
        location=event_schema.location,
        start_date=event_schema.start_date,
        end_date=event_schema.end_date,
    )
    
    db.add(create_event_model)
    db.commit()
    return event_schema


@ router.get("/{event_id}")
async def get_event(
    request: Request,
    event_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    auth_dependency.secure_access("VIEW_EVENT", current_user["user_id"])
    client_ip = dependency.request_ip(request)

    dependency.log_activity(
        current_user['user_id'],
        'VIEW_EVENT',
        current_user['username'],
        client_ip,
        f"View event id {event_id} and associated permissions"
    )

    if event := get_object(event_id, db, Event):
        return {
            "event": {
                "id": event.id,
                "event": event.event,
                "country_id": event.country_id,
                "country": event.country.country,
                "org_unit_id": event.org_unit_id,
                "org_unit": event.org_unit.name,
                "user_id": event.user_id,
                "firstname": event.user.firstname,
                "lastname": event.user.lastname,
                "theme": event.theme,
                "description": event.description,
                "start_date": event.start_date,   
                "end_date": event.end_date,   
            },
            "participants": [
                {
                    "id": participant.id,
                    "user_id": participant.user_id,
                    "firstname": participant.user.firstname,
                    "lastname": participant.user.lastname,
                    "phone": participant.user.phone,
                    "email": participant.user.email,
                }
                for participant in event.registrations
            ],
            "documents": [
                {
                    "id": document.id,
                    "document_type": document.document_type,
                    "file_type": document.file_type,
                    "file_name": document.file_name,
                    "name": document.name,
                    "path": document.path,
                    "access_level": document.access_level,                    
                }
                for document in event.documents
            ],
            "links": [
                {
                    "id": link.id,
                    "name": link.name,
                    "link": link.link,
                }
                for link in event.links
            ],            
        }
    else:
        raise HTTPException(status_code=404, detail="event not found")    
    
@ router.put("/{event_id}")
async def update_event(
    request: Request,
    event_id: int,
    current_user: user_dependency,
    event_schema: EventSchema,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency)
):
    auth_dependency.secure_access(
        "UPDATE_EVENT", current_user["user_id"])

    client_ip = dependency.request_ip(request)

    dependency.log_activity(
        current_user['user_id'],
        'UPDATE_EVENT',
        current_user['username'],
        client_ip,
        f"Update event id {event_id}"
    )
    event_model = get_object(event_id, db, Event)

    event_model.org_unit_id = event_schema.org_unit_id
    event_model.country_id = event_schema.country_id
    event_model.user_id = current_user["user_id"]
    event_model.event = event_schema.event
    event_model.theme = event_schema.theme
    event_model.description = event_schema.description
    event_model.location = event_schema.location
    event_model.start_date = event_schema.start_date
    event_model.end_date = event_schema.end_date
        
    db.commit()
    db.refresh(event_model)
    return event_schema


@ router.delete("/{event_id}")
async def delete_event(
    request: Request,
    event_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency)
):
    auth_dependency.secure_access(
        "DELETE_EVENT", current_user["user_id"])

    dependency.cascade_soft_delete_recursive(Event, event_id)

    client_ip = dependency.request_ip(request)
    event = get_object(event_id, db, Event)

    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        current_user['user_id'],
        'DELETE_EVENT',
        current_user['username'],
        client_ip,
        f"Delete event id {event_id} event {event.event}"
    )
    return {"detail": "event Successfully deleted"}

@ router.post("/registration/")
async def event_registration(
    request: Request,
    registration_schema: RegistrationSchema,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        current_user['user_id'],
        'ADD_EVENT',
        current_user['username'],
        client_ip,
        registration_schema.event_id
    )

    create_registration_model = Registration(
        country_id=registration_schema.country_id,
        user_id=registration_schema.user_id,
        event_id=registration_schema.event_id,
        participation_role=registration_schema.participation_role,
        organisation=registration_schema.organisation,
        registered_at=datetime.now(),
        # payment_date=registration_schema.payment_date,
        # payment_method=registration_schema.payment_method,
        # payment_reference=registration_schema.payment_reference,
        # payment_amount=registration_schema.payment_amount,
        # payment_status=registration_schema.payment_status,
        # payment_receipt=registration_schema.payment_receipt, 
    )
    
    db.add(create_registration_model)
    db.commit()
    return registration_schema


@router.post("/upload_document/")
async def upload_document(
    user: user_dependency,
    file: UploadFile = File(...),
    file_name: str = Form(...),
    doc_type: str = Form(...),
    access_level: str = Form(...),
    event_id: int = Form(...),
    db: Session = Depends(get_db),
):
    try:
        unique_dir = os.path.join(
            EVENT_DOCUMENT_DIR,
            f"{event_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"
        )
        os.makedirs(unique_dir, exist_ok=True)
        file_path = os.path.join(unique_dir, file.filename)
        with open(file_path, "wb+") as file_object:
            file_object.write(await file.read())

        event_document_model = Document(
            event_id=event_id,
            document_type=doc_type,
            file_type=file.content_type,
            file_name=file.filename,
            name=file_name,
            path=file_path,
            access_level=access_level,
        )
        db.add(event_document_model)
        db.commit()
        db.refresh(event_document_model)

        return JSONResponse(
            content={
                "status": "success",
                "message": f"File '{file.filename}' uploaded to '{unique_dir}'",
                "file_path": file_path,
            },
            status_code=200,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/delete_document/{document_id}")
async def delete_document(
    request: Request,
    document_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency)
):
    auth_dependency.secure_access(
        "DELETE_EVENT", current_user["user_id"])    
    
    document = get_object(document_id, db, Document)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    document_folder = os.path.dirname(document.path)
    if os.path.exists(document_folder):
        try:
            shutil.rmtree(document_folder)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete folder: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail="Folder not found on disk")

    db.delete(document)
    db.commit()

    return {"status": "success", "message": f"Document and folder deleted successfully"}


@ router.post("/add_link/")
async def add_link(
    request: Request,
    link_schema: LinkSchema,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        current_user['user_id'],
        'ADD_EVENT',
        current_user['username'],
        client_ip,
        link_schema.event_id
    )

    create_event_link_model = Link(
        event_id=link_schema.event_id,
        name=link_schema.name,
        link=str(link_schema.link),
    )
    
    db.add(create_event_link_model)
    db.commit()
    return link_schema    

@ router.put("/update_link/{link_id}")
async def update_link(
    request: Request,
    link_id: int,
    current_user: user_dependency,
    link_schema: LinkSchema,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency)
):
    auth_dependency.secure_access(
        "UPDATE_EVENT", current_user["user_id"])

    client_ip = dependency.request_ip(request)

    dependency.log_activity(
        current_user['user_id'],
        'UPDATE_EVENT',
        current_user['username'],
        client_ip,
        f"Update event id {link_id}"
    )
    link_model = get_object(link_id, db, Link)

    link_model.name = link_schema.name
    link_model.link = str(link_schema.link)
        
    db.commit()
    db.refresh(link_model)
    return link_schema

@ router.delete("/delete_link/{link_id}")
async def delete_link(
    request: Request,
    link_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency)
):
    auth_dependency.secure_access(
        "DELETE_EVENT", current_user["user_id"])

    dependency.hard_delete(Link, link_id)

    client_ip = dependency.request_ip(request)
    link = get_object(link_id, db, Link)

    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        current_user['user_id'],
        'DELETE_EVENT',
        current_user['username'],
        client_ip,
        f"Delete event id {link} event {link.name}"
    )
    return {"detail": "link Successfully deleted"}