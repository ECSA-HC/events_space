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
from models.models import Event, User, Registration, Document,Link, UserProfile
from schemas.events_space import EventSchema, RegistrationSchema, LinkSchema

from fastapi.responses import StreamingResponse
import io
import openpyxl

from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from io import BytesIO
from typing import Literal
from fastapi import Query

import unicodedata
import re
import urllib.parse



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

def sanitize_filename(name: str) -> str:
    # Normalize to remove accents
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    # Replace spaces and remove non-word characters
    name = re.sub(r"[^\w\s-]", "", name).strip().replace(" ", "_")
    return name

@router.get("/")
async def get_events(
    request: Request,
    db: Session = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = 10,
    search: str = "",
    dependency: Dependency = Depends(get_dependency),
):
    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        1,
        'VIEW_EVENTS',
        "None",
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
    events = events_query.offset(skip).limit(limit).all()

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
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
):
    client_ip = dependency.request_ip(request)

    dependency.log_activity(
        1,
        'VIEW_EVENT',
        "None",
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
                "location": event.location,
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
                    "photo": participant.user.user_photo if participant.user.user_photo else None,
                    "country_id": participant.country_id,
                    "country": participant.country.country,
                    "participation_role": participant.participation_role,
                    "organisation": participant.organisation,  
                    "paid": participant.paid if hasattr(participant, 'paid') else None,
                    "registered_at": participant.registered_at, 
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


@router.post("/registration/")
async def event_registration(
    request: Request,
    registration_schema: RegistrationSchema,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        1,
        'ADD_EVENT',
        registration_schema.email,
        client_ip,
        registration_schema.event_id
    )

    # Check if user exists
    user = db.query(User).filter(User.email == registration_schema.email).first()

    if user is None:
        # Create new user
        role = auth_dependencies.get_user_role('User')
        hashed_password = auth_dependencies.hash_password("defaultpassword123")  # or generate one securely
        user = User(
            firstname=registration_schema.firstname,
            lastname=registration_schema.lastname,
            phone=registration_schema.phone,
            email=registration_schema.email,
            hashed_password=hashed_password,
            verified=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    else:
        # Update user info
        user.firstname = registration_schema.firstname
        user.lastname = registration_schema.lastname
        user.phone = registration_schema.phone
        db.commit()

    # Handle user profile
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    if profile:
        # Update existing profile
        profile.country_id = registration_schema.country_id
        profile.title = registration_schema.title
        profile.middle_name = registration_schema.middle_name
        profile.gender = registration_schema.gender
    else:
        # Create profile
        profile = UserProfile(
            user_id=user.id,
            country_id=registration_schema.country_id,
            title=registration_schema.title,
            middle_name=registration_schema.middle_name,
            gender=registration_schema.gender,
        )
        db.add(profile)
    db.commit()

    # Check if registration already exists
    existing_registration = db.query(Registration).filter(
        Registration.user_id == user.id,
        Registration.event_id == registration_schema.event_id
    ).first()

    if existing_registration:
        raise HTTPException(
            status_code=409,
            detail="User already registered for this event."
        )

    # Create new registration
    new_registration = Registration(
        user_id=user.id,
        country_id=registration_schema.country_id,
        event_id=registration_schema.event_id,
        participation_role=registration_schema.participation_role,  
        profession=registration_schema.profession,
        position=registration_schema.position,      
        organisation=registration_schema.organisation,
    )
    db.add(new_registration)
    db.commit()
    db.refresh(new_registration)

    return {"message": "Registration successful", "registration_id": new_registration.id}


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


@router.get("/{event_id}/participants/download")
async def download_event_participants(
    request: Request,
    event_id: int,
    current_user: user_dependency,
    paid: Literal["all", "true", "false"] = Query("all"),
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    auth_dependency.secure_access("VIEW_EVENT", current_user["user_id"])
    client_ip = dependency.request_ip(request)

    dependency.log_activity(
        current_user['user_id'],
        'DOWNLOAD_PARTICIPANTS',
        current_user['username'],
        client_ip,
        f"Downloaded participants for event {event_id} with filter paid={paid}"
    )

    event = get_object(event_id, db, Event)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")

    # Get participants
    participants = [
        {
            "registration_id": participant.id,
            "firstname": participant.user.firstname,
            "lastname": participant.user.lastname,
            "email": participant.user.email,
            "phone": participant.user.phone,
            "organisation": participant.organisation,
            "country": participant.country.country,
            "participation_role": participant.participation_role,
            "paid": participant.paid if hasattr(participant, 'paid') else None,
            "registered_at": participant.registered_at
        }
        for participant in event.registrations
    ]


    # Filter by paid
    if paid != "all":
        is_paid = paid == "true"
        participants = [p for p in participants if p["paid"] == is_paid]

    if not participants:
        raise HTTPException(status_code=404, detail="No participants found")

    # Create Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Participants"

    headers = [
        "ID", "First Name", "Last Name", "Email", "Phone",
        "Organisation", "Country", "Participation Role", "Paid", "Registered At"
    ]
    ws.append(headers)


    for p in participants:
        ws.append([
            p["registration_id"],
            p["firstname"],
            p["lastname"],
            p["email"],
            p["phone"],
            p["organisation"],
            p["country"],
            p["participation_role"].value if hasattr(p["participation_role"], "value") else str(p["participation_role"]),
            "Yes" if p["paid"] else "No",
            p["registered_at"].strftime("%Y-%m-%d %H:%M:%S")
        ])


    # Prepare Excel stream
    file_stream = BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)

    # Sanitize event name for filename
    safe_event_name = sanitize_filename(event.event)
    ascii_filename = f"{safe_event_name}_participants.xlsx"
    utf8_filename = urllib.parse.quote(ascii_filename)

    return StreamingResponse(
        file_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={ascii_filename}; filename*=UTF-8''{utf8_filename}"
        }
    )