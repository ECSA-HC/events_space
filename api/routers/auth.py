import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, joinedload

from core.database import get_db
from dependencies.dependency import Dependency
from dependencies.auth_dependency import Auth
import utils.mailer_util as mailer_util

from models.models import (
    User,
    UserRole,
    PasswordReset,
    AccountVerification,
    Role,
    RolePermission,
)
from schemas.events_space import (
    UserSchema,
    EmailSchema,
    PasswordResetSchema,
    VerificationTokenSchema,
)

router = APIRouter()


def get_dependency(db: Session = Depends(get_db)) -> Dependency:
    return Dependency(db)


def get_auth_dependency(db: Session = Depends(get_db)) -> Auth:
    return Auth(db)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_schema: UserSchema,
    background_tasks: BackgroundTasks,
    dependency: Dependency = Depends(get_dependency),
    auth_dependencies: Auth = Depends(get_auth_dependency),
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter((User.email == user_schema.email) | (User.phone == user_schema.phone))
        .first()
    )

    if existing_user:
        return {
            "user_id": existing_user.id,
            "email": existing_user.email,
            "already_registered": True,
        }

    role = auth_dependencies.get_user_role("User")
    password = auth_dependencies.generate_random_password()
    hashed_password = auth_dependencies.hash_password(password)

    mailer_util.new_account_email(
        user_schema.email, user_schema.firstname, password, background_tasks
    )

    create_user_model = User(
        firstname=user_schema.firstname,
        lastname=user_schema.lastname,
        phone=user_schema.phone,
        email=user_schema.email,
        hashed_password=hashed_password,
        verified=False,
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)

    db.add(UserRole(user_id=create_user_model.id, role_id=role.id))
    db.commit()

    verification_token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=1)
    db.add(
        AccountVerification(
            user_id=create_user_model.id,
            verification_token=verification_token,
            expires_at=expires_at,
        )
    )
    db.commit()

    dependency.log_activity(
        create_user_model.id,
        "USER_REGISTER",
        user_schema.email,
        "127.0.0.1",
        user_schema.email,
    )

    return {
        "user_id": create_user_model.id,
        "email": user_schema.email,
        "already_registered": False,
    }


@router.post("/login")
async def login(
    auth_schema: OAuth2PasswordRequestForm = Depends(),
    dependency: Dependency = Depends(get_dependency),
    auth_dependencies: Auth = Depends(get_auth_dependency),
    db: Session = Depends(get_db),
):
    user = auth_dependencies.authenticate_user(
        auth_schema.username, auth_schema.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user, check your credentials",
        )

    user_with_permissions = (
        db.query(User)
        .options(
            joinedload(User.user_roles)
            .joinedload(UserRole.role)
            .joinedload(Role.role_permissions)
            .joinedload(RolePermission.permission)
        )
        .filter(User.id == user.id)
        .first()
    )

    token = auth_dependencies.create_access_token(
        user.email, user.id, timedelta(minutes=20)
    )

    dependency.log_activity(
        user.id, "USER_LOGIN", user.email, "127.0.0.1", auth_schema.username
    )

    permissions = [
        {
            "permission": rp.permission.permission,
            "permission_code": rp.permission.permission_code,
        }
        for user_role in user_with_permissions.user_roles
        for rp in user_role.role.role_permissions
    ]

    return {
        "user": {
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "phone": user.phone,
            "email": user.email,
            "verified": user.verified,
        },
        "permissions": permissions,
        "access_token": token,
        "token_type": "bearer",
    }


@router.post("/password-reset-link", status_code=200)
async def forgot_password(
    email_schema: EmailSchema,
    background_tasks: BackgroundTasks,
    dependency: Dependency = Depends(get_dependency),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == email_schema.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Email not found"
        )

    now = datetime.utcnow()
    existing_reset = (
        db.query(PasswordReset)
        .filter(
            PasswordReset.user_id == user.id,
            PasswordReset.is_used == False,
            PasswordReset.expires_at > now,
            PasswordReset.deleted_at == None,
        )
        .order_by(PasswordReset.created_at.desc())
        .first()
    )

    if existing_reset:
        reset_token = existing_reset.reset_token
        expires_at = existing_reset.expires_at
    else:
        reset_token = str(uuid.uuid4())
        expires_at = now + timedelta(hours=1)
        db.add(
            PasswordReset(
                user_id=user.id, reset_token=reset_token, expires_at=expires_at
            )
        )
        db.commit()

    dependency.log_activity(
        user.id, "USER_RESET_PASSWORD", user.email, "127.0.0.1", email_schema.email
    )

    mailer_util.reset_password_request_email(
        user.email, user.firstname, reset_token, background_tasks
    )

    return {
        "message": "A password reset link has been sent to your email. Please check your inbox."
    }


@router.post("/reset_password", status_code=status.HTTP_201_CREATED)
async def reset_password(
    password_reset_schema: PasswordResetSchema,
    background_tasks: BackgroundTasks,
    dependency: Dependency = Depends(get_dependency),
    auth_dependencies: Auth = Depends(get_auth_dependency),
    db: Session = Depends(get_db),
):
    reset_entry = (
        db.query(PasswordReset)
        .filter(
            PasswordReset.reset_token == password_reset_schema.rest_token,
            PasswordReset.is_used == False,
            PasswordReset.expires_at > datetime.utcnow(),
        )
        .first()
    )
    if not reset_entry:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == reset_entry.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = auth_dependencies.hash_password(
        password_reset_schema.password
    )
    reset_entry.is_used = True
    db.commit()

    dependency.log_activity(
        user.id,
        "RESET_PASSWORD",
        user.email,
        "127.0.0.1",
        password_reset_schema.rest_token,
    )

    mailer_util.password_reset_email(user.email, user.firstname, background_tasks)

    return {"message": "Password reset successfully"}


@router.post("/verify-email")
async def verify_email(
    verification_token_schema: VerificationTokenSchema,
    background_tasks: BackgroundTasks,
    dependency: Dependency = Depends(get_dependency),
    db: Session = Depends(get_db),
):
    activation_entry = (
        db.query(AccountVerification)
        .filter(
            AccountVerification.verification_token
            == verification_token_schema.verification_token,
            AccountVerification.is_used == False,
            AccountVerification.expires_at > datetime.utcnow(),
        )
        .first()
    )
    if not activation_entry:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == activation_entry.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.verified = True
    activation_entry.is_used = True
    db.commit()

    dependency.log_activity(
        user.id,
        "VERIFY_EMAIL",
        user.email,
        "127.0.0.1",
        verification_token_schema.verification_token,
    )

    mailer_util.account_verification_email(user.email, user.firstname, background_tasks)

    return {"message": "Account verification was successful"}


@router.post("/resend-verification")
async def resend_verification(
    email_schema: EmailSchema,
    background_tasks: BackgroundTasks,
    dependency: Dependency = Depends(get_dependency),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == email_schema.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    verification_token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=1)

    db.add(
        AccountVerification(
            user_id=user.id,
            verification_token=verification_token,
            expires_at=expires_at,
        )
    )
    db.commit()

    dependency.log_activity(
        user.id,
        "RESEND_VERIFICATION_EMAIL",
        user.email,
        "127.0.0.1",
        email_schema.email,
    )

    mailer_util.account_verification_request_email(
        user.email, user.firstname, verification_token, background_tasks
    )

    return {"message": "Verification email sent successfully"}
