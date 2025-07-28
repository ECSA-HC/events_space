import math
import os
import uuid
import shutil
from fastapi.responses import JSONResponse
from schemas.events_space import UserSchema, ProfileSchema, UserRoleSchema
from passlib.hash import bcrypt
import utils.mailer_util as mailer_util
from datetime import datetime
from sqlalchemy import or_
from typing import Annotated
from core.database import get_db
from sqlalchemy.orm import Session
from dependencies.auth_dependency import Auth, get_current_user
from models.models import User, UserPhoto, UserProfile, UserRole
from dependencies.dependency import Dependency
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Query,
    status,
    Request,
    File,
    UploadFile,
    BackgroundTasks,
)

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


def get_dependency(db: Session = Depends(get_db)) -> Dependency:
    return Dependency(db)


def get_auth_dependency(db: Session = Depends(get_db)) -> Auth:
    return Auth(db)


USER_PHOTO_DIR = "uploads/picture/profile_picture/"
if not os.path.exists(USER_PHOTO_DIR):
    os.makedirs(USER_PHOTO_DIR)


def get_object(id, db, model):
    data = db.query(model).filter(model.id == id).first()
    if data is None:
        raise HTTPException(status_code=404, detail=f"ID {id} : Does not exist")
    return data


@router.get("/")
async def get_users(
    request: Request,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = 10,
    search: str = "",
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    auth_dependency.secure_access("VIEW_USER", current_user["user_id"])
    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        current_user["user_id"],
        "VIEW_USERS",
        current_user["username"],
        client_ip,
        "Get all users",
    )

    search_filter = or_(
        User.firstname.ilike(f"%{search}%"),
        User.lastname.ilike(f"%{search}%"),
        User.email.ilike(f"%{search}%"),
    )

    users_query = db.query(User).filter(search_filter)

    total_count = users_query.count()
    users = users_query.offset(skip).limit(limit).all()

    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": users}


@router.post("/")
async def add_user(
    user_schema: UserSchema,
    current_user: user_dependency,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    auth_dependency.secure_access("ADD_USER", current_user["user_id"])

    existing_email = db.query(User).filter(User.email == user_schema.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    existing_phone = db.query(User).filter(User.phone == user_schema.phone).first()
    if existing_phone:
        raise HTTPException(status_code=400, detail="Phone number already exists")

    password = auth_dependency.generate_random_password()

    hashed_password = bcrypt.hash(password)
    create_user_model = User(
        firstname=user_schema.firstname,
        lastname=user_schema.lastname,
        phone=user_schema.phone,
        email=user_schema.email,
        hashed_password=hashed_password,
        verified=1,
    )

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)

    # Send email in background
    background_tasks.add_task(
        mailer_util.new_account_email,
        user_schema.email,
        user_schema.firstname,
        password,
    )

    return user_schema


@router.get("/{user_id}")
async def get_user(
    request: Request,
    user_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    auth_dependency.secure_access("VIEW_USER", current_user["user_id"])

    client_ip = dependency.request_ip(request)

    dependency.log_activity(
        current_user["user_id"],
        "VIEW_USER",
        current_user["username"],
        client_ip,
        f"View user id {user_id} and associated permissions",
    )

    user = get_object(user_id, db, User)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    # Collect roles - adjust this depending on your model setup
    roles = []
    if hasattr(user, "roles"):
        roles = [
            {
                "id": role.id,
                "role": role.role,
                "description": role.description,
            }
            for role in user.roles
        ]
    elif hasattr(user, "user_roles"):
        # If you use a linking table UserRole with 'role' relationship:
        roles = [
            {
                "id": ur.role.id,
                "role": ur.role.role,
                "description": ur.role.description,
            }
            for ur in user.user_roles
        ]

    return {
        "user": {
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "phone": user.phone,
            "email": user.email,
            "roles": roles,
        },
        "profile": (
            {
                "id": user.user_profile[0].id,
                "title": user.user_profile[0].title,
                "middle_name": user.user_profile[0].middle_name,
                "gender": user.user_profile[0].gender,
                "country_id": user.user_profile[0].country_id,
                "country": user.user_profile[0].country.country,
                "organisation": user.user_profile[0].organisation,
                "position": user.user_profile[0].position,
                "profession": user.user_profile[0].profession,
            }
            if user.user_profile
            else None
        ),
        "profile_picture": (
            {
                "id": user.user_photo[0].id,
                "profile_picture": user.user_photo[0].path,
            }
            if user.user_photo
            else None
        ),
        "events": [
            {
                "id": event.events.id,
                "event": event.events.event,
                "country_id": event.events.country_id,
                "country": event.events.country.country,
                "org_unit_id": event.events.org_unit_id,
                "org_unit": event.events.org_unit.name,
                "theme": event.events.theme,
                "description": event.events.description,
                "start_date": event.events.start_date,
                "end_date": event.events.end_date,
                "paid": event.paid,
            }
            for event in user.registrations
        ],
    }


@router.put("/{user_id}")
async def update_user(
    request: Request,
    user_id: int,
    current_user: user_dependency,
    user_schema: UserSchema,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    # auth_dependency.secure_access("UPDATE_ROLE", current_user["user_id"])

    client_ip = dependency.request_ip(request)

    dependency.log_activity(
        current_user["user_id"],
        "UPDATE_USER",
        current_user["username"],
        client_ip,
        f"Update user id {user_id}",
    )
    user_model = get_object(user_id, db, User)

    user_model.firstname = user_schema.firstname
    user_model.lastname = user_schema.lastname
    user_model.phone = user_schema.phone
    user_model.email = user_schema.email

    db.commit()
    db.refresh(user_model)
    return user_schema


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dependency),
    dependency: Dependency = Depends(get_dependency),
):
    auth_dependency.secure_access("DELETE_USER", current_user["user_id"])

    if not (user := get_object(user_id, db, User)):
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}


@router.post("/roles/")
async def add_user_role(
    user_role_schema: UserRoleSchema,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    auth_dependency.secure_access("ADD_USER", current_user["user_id"])

    # Check if role already assigned to user
    existing = (
        db.query(UserRole)
        .filter(
            UserRole.user_id == user_role_schema.user_id,
            UserRole.role_id == user_role_schema.role_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400, detail="User already has this role assigned"
        )

    user_role = UserRole(
        user_id=user_role_schema.user_id, role_id=user_role_schema.role_id
    )
    db.add(user_role)
    db.commit()
    db.refresh(user_role)
    return {"detail": "User role assigned successfully", "user_role_id": user_role.id}


@router.delete("/roles/")
async def delete_user_role(
    user_role_schema: UserRoleSchema,  # receive user_id and role_id in body
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dependency),
    dependency: Dependency = Depends(get_dependency),
):
    auth_dependency.secure_access("DELETE_USER", current_user["user_id"])

    # Find the UserRole record matching user_id and role_id from body
    user_role = (
        db.query(UserRole)
        .filter(
            UserRole.user_id == user_role_schema.user_id,
            UserRole.role_id == user_role_schema.role_id,
        )
        .first()
    )

    if not user_role:
        raise HTTPException(status_code=404, detail="User role not found")

    db.delete(user_role)
    db.commit()

    return {"detail": "User role deleted successfully"}


@router.post("/profile/{user_id}")
async def add_or_update_profile(
    request: Request,
    user_id: int,
    profile_schema: ProfileSchema,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
):
    client_ip = dependency.request_ip(request)

    # Log the activity
    dependency.log_activity(
        user_id,
        "UPDATE_USER_PROFILE",
        profile_schema.middle_name,  # Or any other identifier
        client_ip,
        f"Update or create profile for user id {user_id}",
    )

    # Check if profile already exists for this user
    profile_model = (
        db.query(UserProfile).filter_by(user_id=user_id, deleted_at=None).first()
    )

    if profile_model:
        # Update existing profile
        profile_model.title = profile_schema.title
        profile_model.middle_name = profile_schema.middle_name
        profile_model.gender = profile_schema.gender
        profile_model.country_id = profile_schema.country_id
        profile_model.organisation = profile_schema.organisation
        profile_model.position = profile_schema.position
        profile_model.profession = profile_schema.profession
    else:
        # Create new profile
        profile_model = UserProfile(
            user_id=user_id,
            title=profile_schema.title,
            middle_name=profile_schema.middle_name,
            gender=profile_schema.gender,
            country_id=profile_schema.country_id,
            organisation=profile_schema.organisation,
            position=profile_schema.position,
            profession=profile_schema.profession,
        )
        db.add(profile_model)

    db.commit()
    db.refresh(profile_model)

    return {
        "user_id": user_id,
        "profile_id": profile_model.id,
        "status": "updated" if profile_model else "created",
        "data": profile_schema.dict(),
    }


@router.put("/profile/{profile_id}")
async def update_profile(
    request: Request,
    profile_id: int,
    current_user: user_dependency,
    profile_schema: ProfileSchema,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    # auth_dependency.secure_access("UPDATE_ROLE", current_user["user_id"])

    client_ip = dependency.request_ip(request)

    dependency.log_activity(
        current_user["user_id"],
        "UPDATE_USER",
        current_user["username"],
        client_ip,
        f"Update user id {profile_id}",
    )
    profile_model = get_object(profile_id, db, UserProfile)

    profile_model.title = profile_schema.title
    profile_model.middle_name = profile_schema.middle_name
    profile_model.gender = profile_schema.gender
    profile_model.country_id = profile_schema.country_id
    profile_model.organisation = profile_schema.organisation
    profile_model.position = profile_schema.position
    profile_model.profession = profile_schema.profession

    db.commit()
    db.refresh(profile_model)
    return profile_schema


@router.post("/upload_user_photo/")
async def upload_user_photo(
    current_user: user_dependency,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        user_id = current_user["user_id"]

        # 1. Query all photos for this user
        existing_photos = db.query(UserPhoto).filter(UserPhoto.user_id == user_id).all()

        # 2. Delete files from filesystem
        for photo in existing_photos:
            if os.path.exists(photo.path):
                # If photo.path is a file path, delete file
                if os.path.isfile(photo.path):
                    os.remove(photo.path)
                # If photo.path is a directory, delete directory recursively
                elif os.path.isdir(photo.path):
                    shutil.rmtree(photo.path)

        # 3. Delete photo records from DB
        db.query(UserPhoto).filter(UserPhoto.user_id == user_id).delete()
        db.commit()

        # 4. Upload new photo
        unique_dir = os.path.join(
            USER_PHOTO_DIR,
            f"{user_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}",
        )
        os.makedirs(unique_dir, exist_ok=True)
        file_path = os.path.join(unique_dir, file.filename)
        with open(file_path, "wb+") as file_object:
            file_object.write(await file.read())

        user_photo_model = UserPhoto(
            user_id=user_id,
            path=file_path,
        )
        db.add(user_photo_model)
        db.commit()
        db.refresh(user_photo_model)

        return JSONResponse(
            content={
                "status": "success",
                "message": f"Photo '{file.filename}' uploaded to '{unique_dir}'",
                "file_path": file_path,
            },
            status_code=200,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/delete_user_photo/{user_photo_id}")
async def delete_profile_picture(
    request: Request,
    user_photo_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    client_ip = dependency.request_ip(request)
    user_photo = get_object(user_photo_id, db, UserPhoto)

    dependency.log_activity(
        current_user["user_id"],
        "DELETE_PHOTO",
        current_user["username"],
        client_ip,
        f"Delete user photo with user id {user_photo.user_id} and photo id {user_photo.id}",
    )

    if not user_photo:
        raise HTTPException(status_code=404, detail="User photo not found")
    user_photo_folder = os.path.dirname(user_photo.path)
    if os.path.exists(user_photo_folder):
        try:
            shutil.rmtree(user_photo_folder)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete folder: {str(e)}"
            )
    else:
        raise HTTPException(status_code=404, detail="Folder not found on disk")

    dependency.hard_delete(UserPhoto, user_photo_id)

    return {
        "status": "success",
        "message": f"User photo and folder deleted successfully",
    }
