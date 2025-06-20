

import math, os
import uuid
import shutil
from fastapi.responses import JSONResponse
from schemas.events_space import UserSchema, UserRoleSchema
from passlib.hash import bcrypt
import utils.mailer_util as mailer_util
from datetime import datetime, timedelta    
from sqlalchemy import or_
from starlette import status
from typing import Annotated
from core.database import get_db
from sqlalchemy.orm import Session
from dependencies.auth_dependency import Auth
from models.models import User, UserRole, UserPhoto
from dependencies.dependency import Dependency
from dependencies.auth_dependency import get_current_user
from schemas.events_space import RoleSchema, RolePermissionSchema
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Query,
    status, Request, HTTPException,File,Form,UploadFile
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
        raise HTTPException(
            status_code=404, detail=f"ID {id} : Does not exist")
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
        current_user['user_id'],
        'VIEW_USERS',
        current_user['username'],
        client_ip,
        "Get all users"
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
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_USER", current_user["user_id"], db)

    existing_email = db.query(Users).filter(
        Users.email == user_schema.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    existing_phone = db.query(Users).filter(
        Users.phone == user_schema.phone).first()
    if existing_phone:
        raise HTTPException(
            status_code=400, detail="Phone number already exists")

    password = mailer_util.generate_random_password()

    hashed_password = bcrypt.hash(password)
    create_user_model = Users(
        firstname=user_schema.firstname,
        lastname=user_schema.lastname,
        phone=user_schema.phone,
        email=user_schema.email,
        hashed_password=hashed_password,
        verified=1,
    )

    db.add(create_user_model)
    db.commit()
    mailer_util.new_account_email(
        user_schema.email, user_schema.firstname, password)
    return user_schema

@ router.get("/{user_id}")
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
        current_user['user_id'],
        'VIEW_USER',
        current_user['username'],
        client_ip,
        f"View user id {user_id} and associated permissions"
    )

    if user := get_object(user_id, db, User):
        return {
            "event": {
                "id": user.id,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "phone": user.phone,
                "email": user.email,   
            },
            "profile_picture": [
                {
                    "id": profile_picture.id,
                    "profile_picture": profile_picture.path,                 
                }
                for profile_picture in user.user_photo
            ],
            "events": [
                {
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
                }
                for event in user.events
            ],          
        }
    else:
        raise HTTPException(status_code=404, detail="user not found")  

@router.post("/upload_user_photo/")
async def upload_user_photo(
    current_user: user_dependency,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        unique_dir = os.path.join(
            USER_PHOTO_DIR,
            f"{current_user["user_id"]}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"
        )
        os.makedirs(unique_dir, exist_ok=True)
        file_path = os.path.join(unique_dir, file.filename)
        with open(file_path, "wb+") as file_object:
            file_object.write(await file.read())

        user_photo_model = UserPhoto(
            user_id = current_user["user_id"],
            path = file_path,
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
    
@ router.delete("/delete_user_photo/{user_photo_id}")
async def delete_profile_picture(
    request: Request,
    user_photo_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency)
):
    client_ip = dependency.request_ip(request)
    user_photo = get_object(user_photo_id, db, UserPhoto)
    
    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        current_user['user_id'],
        'DELETE_PHOTO',
        current_user['username'],
        client_ip,
        f"Delete user photo with user id {user_photo.user_id} and photo id {user_photo.id}"
    )
    
    if not user_photo:
        raise HTTPException(status_code=404, detail="User photo not found")
    user_photo_folder = os.path.dirname(user_photo.path)
    if os.path.exists(user_photo_folder):
        try:
            shutil.rmtree(user_photo_folder)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete folder: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail="Folder not found on disk")

    dependency.hard_delete(UserPhoto, user_photo_id)

    return {"status": "success", "message": f"User photo and folder deleted successfully"}    
     
# @router.get("/{user_id}")
# async def get_user(
#     user_id: int,
#     user: user_dependency,
#     db: Session = Depends(get_db),
# ):
#     security.secureAccess("VIEW_USER", user["id"], db)
#     model = Users
#     user = get_object(user_id, db, model)

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     return {
#         "user": {
#             "id": user.id,
#             "firstname": user.firstname,
#             "lastname": user.lastname,
#             "phone": user.phone,
#             "email": user.email,
#             "participant": user.participant,
#         },
#         "roles": [
#             {
#                 "id": role.id,
#                 "role_id": role.role.id,
#                 "role": role.role.role,
#             }
#             for role in user.user_role
#         ],
#         "events": [
#             {
#                 "id": event.id,
#                 # "file_name": signature.file_name,
#                 # "file_location": signature.file_location,
#             }
#             for event in user.user_event
#         ],
#     }


# @router.put("/{user_id}")
# async def update_user(
#     user_id: int,
#     user: user_dependency,
#     user_schema: UserSchema,
#     db: Session = Depends(get_db),
# ):
#     security.secureAccess("UPDATE_USER", user["id"], db)
#     user_model = get_object(user_id, db, Users)

#     user_model.firstname = user_schema.firstname
#     user_model.lastname = user_schema.lastname
#     user_model.phone = user_schema.phone
#     user_model.email = user_schema.email

#     db.commit()
#     db.refresh(user_model)
#     return user_schema


# @router.delete("/{user_id}")
# async def delete_user(
#     user_id: int,
#     user: user_dependency,
#     db: Session = Depends(get_db),
# ):
#     security.secureAccess("DELETE_USER", user["id"], db)
#     get_object(user_id, db, Users)
#     db.query(Users).filter(Users.id == user_id).delete()
#     db.commit()
#     raise HTTPException(
#         status_code=status.HTTP_200_OK, detail="Users Successfully deleted"
#     )


# @router.put("/password/{user_id}")
# async def update_password(
#     user_id: int,
#     user: user_dependency,
#     db: Session = Depends(get_db),
# ):
#     security.secureAccess("UPDATE_USER", user["id"], db)
#     user = get_object(user_id, db, Users)
#     password = mailer_util.generate_random_password()

#     db.query(Users).filter(Users.id == user_id).update(
#         {"hashed_password": mailer_util.hash_password(password)}
#     )
#     db.commit()
#     # Send a confirmation email (you can customize this part)
#     mailer_util.password_change_email(user.email, user.firstname, password)
#     raise HTTPException(
#         status_code=200, detail="Password updated successfully")


# @router.put("/reset_password/{user_id}")
# async def reset_password(
#     user_id: int,
#     user: user_dependency,
#     password_schema: PasswordSchema,
#     db: Session = Depends(get_db),
# ):
#     security.secureAccess("UPDATE_USER", user["id"], db)
#     user = get_object(user_id, db, Users)
#     password = password_schema.password

#     db.query(Users).filter(Users.id == user_id).update(
#         {"hashed_password": mailer_util.hash_password(password)}
#     )
#     db.commit()
#     # Send a confirmation email (you can customize this part)
#     mailer_util.password_change_email(user.email, user.firstname, password)
#     raise HTTPException(
#         status_code=200, detail="Password rest was successfull")


# @router.post("/roles/")
# async def add_user_role(
#     user_role_schema: UserRoleSchema,
#     user: user_dependency,
#     db: Session = Depends(get_db),
# ):
#     security.secureAccess("ADD_USER", user["id"], db)
#     user_role_model = UserRole(
#         user_id=user_role_schema.user_id, role_id=user_role_schema.role_id
#     )

#     db.add(user_role_model)
#     db.commit()
#     db.refresh(user_role_model)
#     return user_role_model


# @router.put("/roles/{user_role_id}")
# async def update_user_role(
#     user_role_id: int,
#     user_role_schema: UserRoleSchema,
#     user: user_dependency,
#     db: Session = Depends(get_db),
# ):
#     security.secureAccess("UPDATE_USER", user["id"], db)
#     user_role_model = db.query(UserRole).filter(
#         UserRole.id == user_role_id).first()
#     user_role_model.user_id = (user_role_schema.user_id,)
#     user_role_model.role_id = user_role_schema.role_id
#     db.add(user_role_model)
#     db.commit()
#     db.refresh(user_role_model)
#     return user_role_model


# @router.delete("/roles/{user_role_id}")
# async def delete_user_role(
#     user_role_id: int,
#     user: user_dependency,
#     db: Session = Depends(get_db),
# ):
#     security.secureAccess("DELETE_USER", user["id"], db)

#     db.query(UserRole).filter(UserRole.id == user_role_id).delete()
#     db.commit()
#     raise HTTPException(
#         status_code=200, detail="Users role successfully deleted")
