import math, os
from pydantic import BaseModel
import uuid
import shutil
from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from io import BytesIO
from typing import Literal
from fastapi.responses import JSONResponse
from sqlalchemy import or_
from fastapi import status, HTTPException, File, Form, UploadFile
from typing import Annotated
from core.database import get_db
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from dependencies.auth_dependency import Auth
from dependencies.dependency import Dependency
from dependencies.auth_dependency import get_current_user, get_optional_current_user
from typing import Optional
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends, Query, Request
from models.models import Event, User, Registration, Document, Link, Payment, ParticipationRole
from schemas.events_space import EventSchema, EventUpdateSchema, RegistrationSchema, LinkSchema, PaymentSubmitSchema
from PIL import Image
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
import qrcode
from fastapi.responses import StreamingResponse
from reportlab.pdfgen import canvas
import unicodedata
import re
import urllib.parse


router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


def get_dependency(db: Session = Depends(get_db)) -> Dependency:
    return Dependency(db)


def get_auth_dependency(db: Session = Depends(get_db)) -> Auth:
    return Auth(db)


CLIENT_ORIGIN = os.getenv("CLIENT_ORIGIN", "unknown_origin")


EVENT_DOCUMENT_DIR = "uploads/event/documents"
if not os.path.exists(EVENT_DOCUMENT_DIR):
    os.makedirs(EVENT_DOCUMENT_DIR)

EVENT_BANNER_DIR = "uploads/event/banners"
if not os.path.exists(EVENT_BANNER_DIR):
    os.makedirs(EVENT_BANNER_DIR)

ORG_UNIT_LOGO_DIR = "uploads/org_unit/logos"
if not os.path.exists(ORG_UNIT_LOGO_DIR):
    os.makedirs(ORG_UNIT_LOGO_DIR)


def get_object(id: int, db: Session, model):
    data = db.query(model).filter(model.id == id).first()
    if data is None:
        raise HTTPException(
            status_code=404,
            detail=f"{model.__name__} with ID {id} does not exist or has been deleted",
        )
    return data


def sanitize_filename(name: str) -> str:
    # Normalize to remove accents
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    # Replace spaces and remove non-word characters
    name = re.sub(r"[^\w\s-]", "", name).strip().replace(" ", "_")
    return name


# Define mapping of participation_role keys to display names
PARTICIPATION_ROLE_MAP = {
    "secretariat": "ECSA-HC secretariat",
    "moh": "Country delegate (from Ministry of Health)",
    "member_state": "Participant from ECSA Member States",
    "other_africa": "Participant from other African countries",
    "world": "Participant from the Rest of the World",
    "student": "Student",
    "exibitor": "Sponsor/Exhibitor",
}


def convert_png_to_rgb(path):
    img = Image.open(path)
    if img.mode in ("RGBA", "LA"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
        return ImageReader(background)
    return ImageReader(img)


def normalize_event_name(name: str) -> str:
    return (
        name.replace("ᵗʰ", "th")
        .replace("ˢᵗ", "st")
        .replace("ⁿᵈ", "nd")
        .replace("ʳᵈ", "rd")
    )


# ── Badge role colours / labels (matching official ECSA name-tag templates) ───
BADGE_ROLE_COLORS = {
    "media":        "#FFD700",
    "moderator":    "#F7941D",
    "secretariat":  "#00AEEF",
    "speaker":      "#C8102E",
    "presenter":    "#C8102E",
    "delegate":     "#009639",
    "moh":          "#009639",
    "member_state": "#009639",
    "other_africa": "#009639",
    "world":        "#009639",
    "student":      "#009639",
    "participant":  "#009639",
    "exhibitor":    "#F7941D",
    "sponsor":      "#F7941D",
}

BADGE_ROLE_LABELS = {
    "media":        "MEDIA",
    "moderator":    "MODERATOR",
    "secretariat":  "SECRETARIAT",
    "speaker":      "SPEAKER",
    "presenter":    "PRESENTER",
    "delegate":     "DELEGATE",
    "moh":          "DELEGATE",
    "member_state": "DELEGATE",
    "other_africa": "DELEGATE",
    "world":        "DELEGATE",
    "student":      "STUDENT",
    "participant":  "PARTICIPANT",
    "exhibitor":    "EXHIBITOR",
    "sponsor":      "SPONSOR",
}

# ISO 3166-1 alpha-2 codes for ECSA member states shown on the badge
ECSA_FLAG_CODES = ["sz", "ke", "ls", "mw", "mu", "tz", "ug", "zm", "zw"]
_FLAG_CACHE: dict = {}


def _get_flag_images():
    """Return a {code: ImageReader} dict for ECSA member flags (cached)."""
    global _FLAG_CACHE
    if _FLAG_CACHE:
        return _FLAG_CACHE
    flags_dir = "assets/flags"
    os.makedirs(flags_dir, exist_ok=True)
    from urllib.request import urlretrieve
    result = {}
    for code in ECSA_FLAG_CODES:
        local = f"{flags_dir}/{code}.png"
        if not os.path.exists(local):
            try:
                urlretrieve(f"https://flagcdn.com/40x30/{code}.png", local)
            except Exception:
                result[code] = None
                continue
        try:
            result[code] = convert_png_to_rgb(local)
        except Exception:
            result[code] = None
    _FLAG_CACHE = result
    return result


def _fmt_event_dates(event) -> str:
    """Return a human-readable date range for an event."""
    def _fmt(d):
        try:
            return d.strftime("%-d %B %Y")
        except Exception:
            return str(d)
    if event.start_date and event.end_date:
        return f"{_fmt(event.start_date)} – {_fmt(event.end_date)}"
    if event.start_date:
        return _fmt(event.start_date)
    return ""


@router.get("")
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
    dependency.log_activity(1, "VIEW_EVENTS", "None", client_ip, "Get all events")

    search_filter = or_(
        Event.event.ilike(f"%{search}%"),
        Event.theme.ilike(f"%{search}%"),
        Event.description.ilike(f"%{search}%"),
    )

    filters = [Event.deleted_at.is_(None)]
    if search_filter is not None:
        filters.insert(0, search_filter)

    events_query = db.query(Event).options(joinedload(Event.org_unit)).filter(*filters)

    total_count = events_query.count()
    events = events_query.offset(skip).limit(limit).all()

    pages = math.ceil(total_count / limit)
    return {
        "pages": pages,
        "data": [
            {
                "id": e.id,
                "event": e.event,
                "theme": e.theme,
                "description": e.description,
                "start_date": e.start_date,
                "end_date": e.end_date,
                "location": e.location,
                "banner_image": e.banner_image,
                "organizers": e.organizers,
                "org_unit_id": e.org_unit_id,
                "org_unit": {
                    "id": e.org_unit.id,
                    "name": e.org_unit.name,
                    "primary_color": e.org_unit.primary_color or "#0095B6",
                    "secondary_color": e.org_unit.secondary_color or "#F7941D",
                    "logo": e.org_unit.logo,
                } if e.org_unit else None,
                "country_id": e.country_id,
            }
            for e in events
        ],
    }


@router.post("/")
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
        current_user["user_id"],
        "ADD_EVENT",
        current_user["username"],
        client_ip,
        event_schema.event,
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
        banner_image=event_schema.banner_image,
        organizers=event_schema.organizers,
        participation_info=event_schema.participation_info,
        logistics_info=event_schema.logistics_info,
        sponsors_info=event_schema.sponsors_info,
    )

    db.add(create_event_model)
    db.commit()
    db.refresh(create_event_model)
    return {"id": create_event_model.id}


def _build_pending_list(pending_regs, db):
    """Build pending registration list with abstract_reminder_sent flag."""
    from models.models import EmailLog
    reminded_emails = {
        row.recipient_email.lower()
        for row in db.query(EmailLog.recipient_email)
        .filter(EmailLog.email_type == "registration_reminder", EmailLog.status == "sent")
        .all()
    }
    return [
        {
            "id": r.id,
            "user_id": r.user_id,
            "firstname": r.user.firstname if r.user else None,
            "lastname": r.user.lastname if r.user else None,
            "email": r.user.email if r.user else None,
            "phone": r.user.phone if r.user else None,
            "country": (
                r.user.user_profile[0].country.country
                if r.user and r.user.user_profile and r.user.user_profile[0].country
                else None
            ),
            "participation_role": r.participation_role,
            "registered_at": r.registered_at,
            "abstract_reminder_sent": (r.user.email or "").lower() in reminded_emails,
        }
        for r in pending_regs
    ]


@router.get("/{event_id}")
async def get_event(
    request: Request,
    event_id: int,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    current_user: Optional[dict] = Depends(get_optional_current_user),
):
    client_ip = dependency.request_ip(request)

    dependency.log_activity(
        1,
        "VIEW_EVENT",
        "None",
        client_ip,
        f"View event id {event_id} and associated permissions",
    )

    if event := get_object(event_id, db, Event):
        _all_regs = event.registrations or []
        # Confirmed = paid OR has uploaded proof; pending = neither
        registrations = [r for r in _all_regs if r.paid or r.payment_proof]
        pending_payment_regs = [r for r in _all_regs if not r.paid and not r.payment_proof]
        documents = event.documents or []
        links = event.links or []

        # ── Determine the current user's access level ─────────────────────────
        # "none"   → not logged in
        # "unpaid" → logged in but no paid registration for this event
        # "paid"   → has a paid registration OR has admin/secretariat permission
        user_access = "none"
        if current_user:
            uid = current_user["user_id"]
            # Check for admin permission (ADMIN_DASHBOARD) → always full access
            from models.models import UserRole, RolePermission, Permission as Perm
            is_admin = db.query(UserRole).join(
                RolePermission, UserRole.role_id == RolePermission.role_id
            ).join(
                Perm, RolePermission.permission_id == Perm.id
            ).filter(
                UserRole.user_id == uid,
                Perm.permission_code == "ADMIN_DASHBOARD",
            ).first()

            if is_admin:
                user_access = "paid"
            else:
                reg = db.query(Registration).filter(
                    Registration.user_id == uid,
                    Registration.event_id == event_id,
                    Registration.deleted_at == None,
                ).first()
                if reg and reg.paid:
                    user_access = "paid"
                else:
                    user_access = "unpaid"

        # Fetch payment data via raw SQL to avoid ORM enum conversion errors on legacy data
        from sqlalchemy import text as _sql_text

        # Abstract author registration stats
        _abstract_author_stats = {"total_authors": 0, "registered": 0, "not_registered": 0}
        try:
            _author_rows = db.execute(
                _sql_text(
                    "SELECT DISTINCT LOWER(aa.email) as email"
                    " FROM abstract a"
                    " JOIN abstract_author aa ON aa.abstract_id = a.id"
                    " WHERE a.event_id = :eid AND a.status = 'accepted' AND aa.email IS NOT NULL"
                ),
                {"eid": event_id},
            ).fetchall()
            _total_authors = len(_author_rows)
            if _total_authors:
                _registered_count = db.execute(
                    _sql_text(
                        "SELECT COUNT(DISTINCT LOWER(u.email)) as cnt"
                        " FROM registration r"
                        " JOIN user u ON u.id = r.user_id"
                        " WHERE r.event_id = :eid AND r.deleted_at IS NULL"
                        " AND LOWER(u.email) IN ("
                        "   SELECT DISTINCT LOWER(aa2.email)"
                        "   FROM abstract a2"
                        "   JOIN abstract_author aa2 ON aa2.abstract_id = a2.id"
                        "   WHERE a2.event_id = :eid AND a2.status = 'accepted' AND aa2.email IS NOT NULL"
                        " )"
                    ),
                    {"eid": event_id},
                ).scalar() or 0
                _abstract_author_stats = {
                    "total_authors": _total_authors,
                    "registered": int(_registered_count),
                    "not_registered": _total_authors - int(_registered_count),
                }
        except Exception as _ae:
            logger.error(f"Abstract author stats error: {_ae}")
        _reg_ids = [r.id for r in registrations]
        if _reg_ids:
            _placeholders = ",".join(str(rid) for rid in _reg_ids)
            _payment_rows = db.execute(
                _sql_text(
                    f"SELECT registration_id, payment_method, payment_amount, payment_date"
                    f" FROM payment WHERE registration_id IN ({_placeholders})"
                )
            ).fetchall()
            payment_by_reg = {row.registration_id: row for row in _payment_rows}
        else:
            payment_by_reg = {}

        return {
            "event": {
                "id": event.id,
                "event": event.event,
                "country_id": event.country_id,
                "country": event.country.country if event.country else None,
                "org_unit_id": event.org_unit_id,
                "org_unit": event.org_unit.name if event.org_unit else None,
                "org_unit_primary_color": event.org_unit.primary_color if event.org_unit else "#0095B6",
                "org_unit_secondary_color": event.org_unit.secondary_color if event.org_unit else "#F7941D",
                "org_unit_logo": event.org_unit.logo if event.org_unit else None,
                "user_id": event.user_id,
                "firstname": event.user.firstname if event.user else None,
                "lastname": event.user.lastname if event.user else None,
                "location": event.location,
                "theme": event.theme,
                "description": event.description,
                "start_date": event.start_date,
                "end_date": event.end_date,
                "banner_image": event.banner_image,
                "organizers": event.organizers,
                "participation_info": event.participation_info,
                "logistics_info": event.logistics_info,
                "sponsors_info": event.sponsors_info,
                "participation_role": (
                    registrations[0].participation_role if registrations else None
                ),
                "user_access": user_access,
            },
            "participants": [
                {
                    "id": r.id,
                    "user_id": r.user_id,
                    "firstname": r.user.firstname if r.user else None,
                    "lastname": r.user.lastname if r.user else None,
                    "phone": r.user.phone if r.user else None,
                    "email": r.user.email if r.user else None,
                    "photo": (
                        r.user.user_photo if r.user and r.user.user_photo else None
                    ),
                    "country_id": (
                        r.user.user_profile[0].country_id
                        if r.user and r.user.user_profile
                        else None
                    ),
                    "country": (
                        r.user.user_profile[0].country.country
                        if r.user and r.user.user_profile and r.user.user_profile[0].country
                        else None
                    ),
                    "participation_role": r.participation_role,
                    "organisation": (
                        r.user.user_profile[0].organisation
                        if r.user and r.user.user_profile
                        else None
                    ),
                    "position": (
                        r.user.user_profile[0].position
                        if r.user and r.user.user_profile
                        else None
                    ),
                    "title": (
                        r.user.user_profile[0].title
                        if r.user and r.user.user_profile
                        else None
                    ),
                    "paid": getattr(r, "paid", None),
                    "payment_proof": getattr(r, "payment_proof", None),
                    "payment_method": payment_by_reg[r.id].payment_method if r.id in payment_by_reg else None,
                    "payment_amount": float(payment_by_reg[r.id].payment_amount) if r.id in payment_by_reg and payment_by_reg[r.id].payment_amount else None,
                    "payment_date": str(payment_by_reg[r.id].payment_date) if r.id in payment_by_reg and payment_by_reg[r.id].payment_date else None,
                    "registered_at": r.registered_at,
                    "reminder_sent_at": getattr(r, "reminder_sent_at", None),
                }
                for r in registrations
            ],
            "documents": [
                {
                    "id": d.id,
                    "document_type": d.document_type,
                    "file_type": d.file_type,
                    "file_name": d.file_name,
                    "name": d.name,
                    "path": d.path,
                    "access_level": d.access_level,
                }
                for d in documents
            ],
            "links": [
                {
                    "id": l.id,
                    "name": l.name,
                    "link": l.link,
                }
                for l in links
            ],
            "pending_registrations": _build_pending_list(pending_payment_regs, db),
            "abstract_author_stats": _abstract_author_stats,
        }
    else:
        raise HTTPException(status_code=404, detail="event not found")


@router.put("/{event_id}")
async def update_event(
    request: Request,
    event_id: int,
    current_user: user_dependency,
    event_schema: EventUpdateSchema,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    auth_dependency.secure_access("UPDATE_EVENT", current_user["user_id"])

    client_ip = dependency.request_ip(request)

    dependency.log_activity(
        current_user["user_id"],
        "UPDATE_EVENT",
        current_user["username"],
        client_ip,
        f"Update event id {event_id}",
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
    event_model.organizers = event_schema.organizers
    event_model.participation_info = event_schema.participation_info
    event_model.logistics_info = event_schema.logistics_info
    event_model.sponsors_info = event_schema.sponsors_info
    if event_schema.banner_image is not None:
        event_model.banner_image = event_schema.banner_image

    db.commit()
    db.refresh(event_model)
    return event_schema


@router.delete("/{event_id}")
async def delete_event(
    request: Request,
    event_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    auth_dependency.secure_access("DELETE_EVENT", current_user["user_id"])

    dependency.cascade_soft_delete_recursive(Event, event_id)

    client_ip = dependency.request_ip(request)
    event = get_object(event_id, db, Event)

    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        current_user["user_id"],
        "DELETE_EVENT",
        current_user["username"],
        client_ip,
        f"Delete event id {event_id} event {event.event}",
    )
    return {"detail": "event Successfully deleted"}


@router.get("/registration/{registration_id}")
async def get_registration_details(
    request: Request,
    registration_id: int,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
):
    client_ip = dependency.request_ip(request)

    dependency.log_activity(
        1,
        "VIEW_REGISTRATION",
        "None",
        client_ip,
        f"View registration ID {registration_id}",
    )

    registration = get_object(registration_id, db, Registration)
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    user = db.query(User).filter(User.id == registration.user_id).first()
    event = db.query(Event).filter(Event.id == registration.event_id).first()

    return {
        "registration": {
            "id": registration.id,
            "user_id": registration.user_id,
            "event_id": registration.event_id,
            "participation_role": registration.participation_role.name,
            "paid": registration.paid,
            "created_at": registration.created_at,
            "updated_at": registration.updated_at,
        },
        "user": (
            {
                "id": user.id,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "phone": user.phone,
            }
            if user
            else None
        ),
        "event": (
            {
                "id": event.id,
                "event": event.event,
                "location": event.location,
                "start_date": event.start_date,
                "end_date": event.end_date,
            }
            if event
            else None
        ),
    }


# Maps frontend strings → PaymentMethod enum name (accessed via PaymentMethod[name])
METHOD_MAP = {
    "bank transfer": "BANK_TRANSFER",
    "mpesa": "MPESA",
    "cash": "CASH",
    "card": "CARD",
    "mobile money": "MPESA",
    "credit card": "CARD",
    "debit card": "CARD",
    "online payment (credit/debit card)": "CARD",
    "online": "CARD",
}


@router.post("/payment/")
async def submit_payment(
    registration_id: int = Form(...),
    event_id: int = Form(...),
    payment_method: str = Form(...),
    payment_amount: float = Form(...),
    proof_file: Optional[UploadFile] = File(None),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db),
):
    from models.models import PaymentMethod, PaymentStatus
    from utils.mailer_util import proof_of_payment_received_email

    registration = get_object(registration_id, db, Registration)

    raw_method = payment_method.strip()
    enum_name = METHOD_MAP.get(raw_method.lower())
    if not enum_name:
        raise HTTPException(status_code=422, detail=f"Unknown payment method: {raw_method}")
    method_enum = PaymentMethod[enum_name]

    proof_path = None
    if proof_file and proof_file.filename:
        ext = os.path.splitext(proof_file.filename)[1]
        unique_name = f"proof_{registration_id}_{uuid.uuid4().hex[:8]}{ext}"
        proof_path = os.path.join(PAYMENT_RECEIPT_DIR, unique_name)
        with open(proof_path, "wb+") as f:
            f.write(await proof_file.read())

    auto_ref = f"REF-{uuid.uuid4().hex[:10].upper()}"

    existing = db.query(Payment).filter(
        Payment.registration_id == registration_id
    ).first()

    if existing:
        existing.payment_method = method_enum
        existing.payment_reference = auto_ref
        existing.payment_amount = payment_amount
        existing.payment_date = datetime.utcnow()
        if proof_path:
            registration.payment_proof = proof_path
        db.commit()
        db.refresh(existing)
        try:
            ev = db.query(Event).filter(Event.id == event_id).first()
            if registration.user and registration.user.email:
                proof_of_payment_received_email(
                    recipient_email=registration.user.email,
                    firstname=registration.user.firstname or "Participant",
                    event_name=ev.event if ev else "the event",
                    background_tasks=background_tasks,
                    db=db,
                )
        except Exception:
            pass
        return {"message": "Payment details updated", "payment_id": existing.id}

    new_payment = Payment(
        registration_id=registration_id,
        payment_date=datetime.utcnow(),
        payment_method=method_enum,
        payment_reference=auto_ref,
        payment_amount=payment_amount,
        payment_status=PaymentStatus.PENDING,
    )
    db.add(new_payment)
    if proof_path:
        registration.payment_proof = proof_path
    db.commit()
    db.refresh(new_payment)
    try:
        ev = db.query(Event).filter(Event.id == event_id).first()
        if registration.user and registration.user.email:
            proof_of_payment_received_email(
                recipient_email=registration.user.email,
                firstname=registration.user.firstname or "Participant",
                event_name=ev.event if ev else "the event",
                background_tasks=background_tasks,
                db=db,
            )
    except Exception:
        pass
    return {"message": "Payment submitted successfully", "payment_id": new_payment.id}


@router.post("/register-with-payment/")
async def register_with_payment(
    user_id: int = Form(...),
    event_id: int = Form(...),
    participation_role: str = Form(...),
    payment_method: str = Form(...),
    payment_amount: float = Form(...),
    proof_file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db),
):
    """Create registration + payment record together, only after proof is uploaded."""
    from models.models import PaymentMethod, PaymentStatus, ParticipationRole
    from utils.mailer_util import proof_of_payment_received_email

    # Prevent duplicate registration
    existing = db.query(Registration).filter(
        Registration.user_id == user_id,
        Registration.event_id == event_id,
        Registration.deleted_at == None,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="You are already registered for this event.")

    # Resolve enums
    raw_method = payment_method.strip()
    enum_name = METHOD_MAP.get(raw_method.lower())
    if not enum_name:
        raise HTTPException(status_code=422, detail=f"Unknown payment method: {raw_method}")
    method_enum = PaymentMethod[enum_name]

    try:
        role_enum = ParticipationRole[participation_role]
    except KeyError:
        raise HTTPException(status_code=422, detail=f"Unknown participation role: {participation_role}")

    # Save proof file first
    if not proof_file or not proof_file.filename:
        raise HTTPException(status_code=422, detail="Proof of payment file is required.")
    ext = os.path.splitext(proof_file.filename)[1]
    unique_name = f"proof_new_{user_id}_{event_id}_{uuid.uuid4().hex[:8]}{ext}"
    proof_path = os.path.join(PAYMENT_RECEIPT_DIR, unique_name)
    with open(proof_path, "wb+") as f:
        f.write(await proof_file.read())

    try:
        # Create registration
        new_registration = Registration(
            user_id=user_id,
            event_id=event_id,
            participation_role=role_enum,
            payment_proof=proof_path,
        )
        db.add(new_registration)
        db.flush()

        # Create payment record
        new_payment = Payment(
            registration_id=new_registration.id,
            payment_date=datetime.utcnow(),
            payment_method=method_enum,
            payment_reference=f"REF-{uuid.uuid4().hex[:10].upper()}",
            payment_amount=payment_amount,
            payment_status=PaymentStatus.PENDING,
        )
        db.add(new_payment)
        db.commit()
        db.refresh(new_registration)
        try:
            _user = db.query(User).filter(User.id == user_id).first()
            ev = db.query(Event).filter(Event.id == event_id).first()
            if _user and _user.email:
                proof_of_payment_received_email(
                    recipient_email=_user.email,
                    firstname=_user.firstname or "Participant",
                    event_name=ev.event if ev else "the event",
                    background_tasks=background_tasks,
                    db=db,
                )
        except Exception:
            pass
        return {"message": "Registration and payment proof submitted successfully", "registration_id": new_registration.id}
    except Exception as e:
        db.rollback()
        import os as _os
        if _os.path.exists(proof_path):
            _os.remove(proof_path)
        raise HTTPException(status_code=500, detail="Failed to complete registration. Please try again.") from e


@router.post("/registration/{user_id}")
async def event_registration(
    request: Request,
    user_id: int,
    registration_schema: RegistrationSchema,
    # current_user: user_dependency,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    # auth_dependency: Auth = Depends(get_auth_dependency),
):
    # user = db.query(User).filter(User.id == user_id).first()
    # client_ip = dependency.request_ip(request)

    # dependency.log_activity(
    #     1,
    #     "EVENT_REGISTRATION",
    #     user.email,
    #     client_ip,
    #     f"Event ID: {registration_schema.event_id}",
    # )

    # Check for existing registration
    existing_registration = (
        db.query(Registration)
        .filter(
            Registration.user_id == user_id,
            Registration.event_id == registration_schema.event_id,
        )
        .first()
    )

    if existing_registration:
        # Update existing registration
        existing_registration.participation_role = (
            registration_schema.participation_role
        )
        db.commit()
        db.refresh(existing_registration)
        return {
            "message": "Registration updated successfully",
            "registration_id": existing_registration.id,
        }

    # Create new registration
    new_registration = Registration(
        user_id=user_id,
        event_id=registration_schema.event_id,
        participation_role=registration_schema.participation_role,
    )
    db.add(new_registration)
    db.commit()
    db.refresh(new_registration)

    return {
        "message": "Registration successful",
        "registration_id": new_registration.id,
    }


@router.delete("/registration/{event_id}")
async def event_deregistration(
    request: Request,
    event_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    client_ip = dependency.request_ip(request)

    dependency.log_activity(
        1,
        "EVENT_DEREGISTER",
        "None",
        client_ip,
        f"Deregister event id {event_id}",
    )

    existing_registration = (
        db.query(Registration)
        .filter(
            Registration.user_id == current_user["user_id"],
            Registration.event_id == event_id,
        )
        .first()
    )

    try:
        db.query(Registration).filter(
            Registration.id == existing_registration.id
        ).delete(synchronize_session=False)
        db.commit()
    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user event registration",
        ) from error


PAYMENT_RECEIPT_DIR = "uploads/payment_receipts"
if not os.path.exists(PAYMENT_RECEIPT_DIR):
    os.makedirs(PAYMENT_RECEIPT_DIR)


@router.delete("/deregister_participant/{registration_id}")
async def admin_deregister_participant(
    request: Request,
    registration_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    """Admin-only: deregister any participant by registration ID."""
    auth_dependency.secure_access("ADMIN_DASHBOARD", current_user["user_id"])

    registration = db.query(Registration).filter(Registration.id == registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    try:
        db.query(Registration).filter(
            Registration.id == registration.id
        ).delete(synchronize_session=False)
        db.commit()
    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to deregister participant",
        ) from error

    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        current_user["user_id"],
        "ADMIN_DEREGISTER",
        current_user["username"],
        client_ip,
        f"Admin deregistered registration ID {registration_id}",
    )
    return {"detail": "Participant successfully deregistered"}


@router.post("/upload_payment_proof/{event_id}")
async def upload_payment_proof(
    event_id: int,
    current_user: user_dependency,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """User uploads proof of payment for their registration."""
    registration = db.query(Registration).filter(
        Registration.user_id == current_user["user_id"],
        Registration.event_id == event_id,
        Registration.deleted_at == None,
    ).first()

    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    try:
        ext = os.path.splitext(file.filename)[1]
        unique_name = f"proof_{registration.id}_{uuid.uuid4().hex[:8]}{ext}"
        file_path = os.path.join(PAYMENT_RECEIPT_DIR, unique_name)
        with open(file_path, "wb+") as f:
            f.write(await file.read())

        registration.payment_proof = file_path
        db.commit()

        return JSONResponse(content={"status": "success", "payment_proof": file_path})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/verify_payment/{registration_id}")
async def verify_payment(
    request: Request,
    registration_id: int,
    current_user: user_dependency,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    """Admin verifies a participant's payment, setting paid=True."""
    auth_dependency.secure_access("ADMIN_DASHBOARD", current_user["user_id"])

    registration = db.query(Registration).filter(Registration.id == registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    registration.paid = True

    # Generate a fresh password so credentials are always included in the verified email
    new_plain_password = None
    try:
        new_plain_password = auth_dependency.generate_random_password()
        registration.user.hashed_password = auth_dependency.hash_password(new_plain_password)
        registration.user.must_change_password = True
    except Exception as _pe:
        logger.error(f"Failed to generate password for verified user: {_pe}")

    db.commit()

    try:
        from utils.mailer_util import payment_verified_email
        event = db.query(Event).filter(Event.id == registration.event_id).first()
        if registration.user and registration.user.email and event:
            payment_verified_email(
                recipient_email=registration.user.email,
                firstname=registration.user.firstname or "Participant",
                event_name=event.event,
                password=new_plain_password,
                background_tasks=background_tasks,
                db=db,
                sent_by_user_id=current_user["user_id"],
            )
    except Exception as _e:
        logger.error(f"Failed to send payment verified email: {_e}")

    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        current_user["user_id"],
        "VERIFY_PAYMENT",
        current_user["username"],
        client_ip,
        f"Verified payment for registration ID {registration_id}",
    )
    return {"detail": "Payment verified successfully"}


@router.put("/unverify_payment/{registration_id}")
async def unverify_payment(
    request: Request,
    registration_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    """Admin marks a participant's payment as unpaid."""
    auth_dependency.secure_access("ADMIN_DASHBOARD", current_user["user_id"])

    registration = db.query(Registration).filter(Registration.id == registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    registration.paid = False
    db.commit()

    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        current_user["user_id"],
        "UNVERIFY_PAYMENT",
        current_user["username"],
        client_ip,
        f"Marked payment as unpaid for registration ID {registration_id}",
    )
    return {"detail": "Payment marked as unpaid"}


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
            f"{event_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}",
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


@router.post("/upload_banner/{event_id}")
async def upload_banner(
    event_id: int,
    user: user_dependency,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        ext = os.path.splitext(file.filename)[1]
        unique_name = f"{event_id}_{uuid.uuid4().hex[:8]}{ext}"
        file_path = os.path.join(EVENT_BANNER_DIR, unique_name)
        with open(file_path, "wb+") as f:
            f.write(await file.read())

        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        event.banner_image = file_path
        db.commit()

        return JSONResponse(content={"status": "success", "banner_image": file_path})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete_document/{document_id}")
async def delete_document(
    request: Request,
    document_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    auth_dependency.secure_access("DELETE_EVENT", current_user["user_id"])

    document = get_object(document_id, db, Document)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    document_folder = os.path.dirname(document.path)
    if os.path.exists(document_folder):
        try:
            shutil.rmtree(document_folder)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete folder: {str(e)}"
            )
    else:
        raise HTTPException(status_code=404, detail="Folder not found on disk")

    db.delete(document)
    db.commit()

    return {"status": "success", "message": f"Document and folder deleted successfully"}


@router.post("/add_link/")
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
        current_user["user_id"],
        "ADD_EVENT",
        current_user["username"],
        client_ip,
        link_schema.event_id,
    )

    create_event_link_model = Link(
        event_id=link_schema.event_id,
        name=link_schema.name,
        link=str(link_schema.link),
    )

    db.add(create_event_link_model)
    db.commit()
    return link_schema


@router.put("/update_link/{link_id}")
async def update_link(
    request: Request,
    link_id: int,
    current_user: user_dependency,
    link_schema: LinkSchema,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    auth_dependency.secure_access("UPDATE_EVENT", current_user["user_id"])

    client_ip = dependency.request_ip(request)

    dependency.log_activity(
        current_user["user_id"],
        "UPDATE_EVENT",
        current_user["username"],
        client_ip,
        f"Update event id {link_id}",
    )
    link_model = get_object(link_id, db, Link)

    link_model.name = link_schema.name
    link_model.link = str(link_schema.link)

    db.commit()
    db.refresh(link_model)
    return link_schema


@router.delete("/delete_link/{link_id}")
async def delete_link(
    request: Request,
    link_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    auth_dependency.secure_access("DELETE_EVENT", current_user["user_id"])

    dependency.hard_delete(Link, link_id)

    client_ip = dependency.request_ip(request)
    link = get_object(link_id, db, Link)

    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        current_user["user_id"],
        "DELETE_EVENT",
        current_user["username"],
        client_ip,
        f"Delete event id {link} event {link.name}",
    )
    return {"detail": "link Successfully deleted"}


@router.get("/{event_id}/participants/download")
async def download_event_participants(
    request: Request,
    event_id: int,
    current_user: user_dependency,
    paid: Literal["all", "true", "false"] = Query("all"),
    db: Session = Depends(get_db),
    dependency=Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    # Permission check
    auth_dependency.secure_access("VIEW_EVENT", current_user["user_id"])
    client_ip = dependency.request_ip(request)

    dependency.log_activity(
        current_user["user_id"],
        "DOWNLOAD_PARTICIPANTS",
        current_user["username"],
        client_ip,
        f"Downloaded participants for event {event_id} with filter paid={paid}",
    )

    event = get_object(event_id, db, Event)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Collect participant details
    participants = []
    for reg in event.registrations:
        user = reg.user
        profile = user.user_profile[0] if user.user_profile else None
        country = profile.country.country if profile and profile.country else None
        organisation = profile.organisation if profile else None

        # Convert participation_role to string key (adjust this if ParticipationRole is Enum)
        role_key = (
            reg.participation_role.name
            if hasattr(reg.participation_role, "name")
            else str(reg.participation_role).lower()
        )

        participants.append(
            {
                "registration_id": reg.id,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "phone": user.phone,
                "title": profile.title if profile else "",
                "middle_name": profile.middle_name if profile else "",
                "gender": profile.gender if profile else "",
                "position": profile.position if profile else "",
                "organisation": organisation,
                "country": country,
                "participation_role": PARTICIPATION_ROLE_MAP.get(role_key, role_key),
                "paid": reg.paid,
                "registered_at": reg.registered_at,
            }
        )

    # Filter by paid status
    if paid != "all":
        is_paid = paid == "true"
        participants = [p for p in participants if p["paid"] == is_paid]

    if not participants:
        raise HTTPException(status_code=404, detail="No participants found")

    # Create Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Participants"

    headers = [
        "ID",
        "Title",
        "First Name",
        "Middle Name",
        "Last Name",
        "Gender",
        "Email",
        "Phone",
        "Organisation",
        "Position",
        "Country",
        "Participation Role",
        "Paid",
        "Registered At",
    ]
    ws.append(headers)

    for p in participants:
        ws.append(
            [
                p["registration_id"],
                p["title"],
                p["firstname"],
                p["middle_name"],
                p["lastname"],
                p["gender"],
                p["email"],
                p["phone"],
                p["organisation"] or "",
                p["position"],
                p["country"] or "",
                p["participation_role"],
                "Yes" if p["paid"] else "No",
                p["registered_at"].strftime("%Y-%m-%d %H:%M:%S"),
            ]
        )

    # Stream response
    file_stream = BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)

    safe_event_name = sanitize_filename(event.event)
    ascii_filename = f"{safe_event_name}_participants.xlsx"
    utf8_filename = urllib.parse.quote(ascii_filename)

    return StreamingResponse(
        file_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={ascii_filename}; filename*=UTF-8''{utf8_filename}"
        },
    )


@router.get("/with-registration/{user_id}")
def list_events_with_user_registration(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),  # or your custom dependency
):
    # Get all events
    events = db.query(Event).all()

    # Get all registrations by the user
    user_regs = (
        db.query(Registration)
        .filter(Registration.user_id == user_id, Registration.deleted_at.is_(None))
        .all()
    )

    # Build a lookup dictionary for quick access: event_id -> registration
    reg_map = {reg.event_id: reg for reg in user_regs}

    # Construct result
    result = []
    for event in events:
        registration = reg_map.get(event.id)
        result.append(
            {
                "event": {
                    "id": event.id,
                    "title": event.event,
                    "theme": event.theme,
                    "description": event.description,
                    "start_date": event.start_date,
                    "end_date": event.end_date,
                    "location": event.location,
                    "country": event.country.country if event.country else None,
                    "org_unit": event.org_unit.name if event.org_unit else None,
                },
                "registered": bool(registration),
                "registration_details": (
                    {
                        "registration_id": registration.id,
                        "participation_role": registration.participation_role,
                        "paid": registration.paid,
                        "payment_status": "Paid" if registration.paid else "Not Paid",
                        "registered_at": registration.registered_at,
                    }
                    if registration
                    else None
                ),
            }
        )

    return result


def hex_to_rgb(hex_color: str):
    """Convert a hex color string like '#a02626' to a 0.0-1.0 RGB tuple."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i: i + 2], 16) / 255.0 for i in (0, 2, 4))


def _render_badge_page(c, p, logo_left, logo_right, primary_rgb=None, secondary_rgb=None):
    """Render one A6 ECSA conference badge matching the official name-tag design exactly.

    All positions derived from official ECSA-HC A6 (105×148 mm) badge PDFs.
    PyMuPDF extracted coordinates are in mm from top; converted to ReportLab
    (y from bottom) via fy(y_top_mm) = (148 - y_top_mm) * mm.
    """
    W_mm, H_mm = 105.0, 148.0
    W, H = W_mm * mm, H_mm * mm

    def fy(y_from_top):
        """mm-from-top  →  ReportLab points-from-bottom."""
        return (H_mm - y_from_top) * mm

    # ── Role colour ──────────────────────────────────────────────────────────
    role_raw   = str(p.get("participation_role_raw", "delegate")).lower()
    role_hex   = BADGE_ROLE_COLORS.get(role_raw, "#0095B6")
    role_rgb   = hex_to_rgb(role_hex)
    role_light = tuple(0.80 + v * 0.20 for v in role_rgb)
    banner_txt = (0.0, 0.0, 0.0) if role_hex == "#FFD700" else (1.0, 1.0, 1.0)
    role_label = BADGE_ROLE_LABELS.get(role_raw, role_raw.upper())

    # ── Background texture (grey granite, extracted from official ECSA badge) ─
    bg_path = "assets/badge_bg.jpg"
    if os.path.exists(bg_path):
        try:
            c.drawImage(convert_png_to_rgb(bg_path), 0, 0, W, H)
        except Exception:
            c.setFillColorRGB(0.82, 0.80, 0.78)
            c.rect(0, 0, W, H, fill=True, stroke=False)
    else:
        c.setFillColorRGB(0.82, 0.80, 0.78)
        c.rect(0, 0, W, H, fill=True, stroke=False)

    # ── Logos ─────────────────────────────────────────────────────────────────
    # Left logo (Eswatini MoH): 5–32 mm from left, 3–17 mm from top
    # Right logo (ECSA-HC):    58–98 mm from left, 3–17 mm from top
    logo_h_mm = 14.0
    if logo_left:
        try:
            c.drawImage(logo_left, 5*mm, fy(3 + logo_h_mm),
                        width=27*mm, height=logo_h_mm*mm, preserveAspectRatio=True)
        except Exception:
            pass
    if logo_right:
        try:
            c.drawImage(logo_right, 58*mm, fy(3 + logo_h_mm),
                        width=40*mm, height=logo_h_mm*mm, preserveAspectRatio=True)
        except Exception:
            pass

    # ── Event title ───────────────────────────────────────────────────────────
    # Extracted: title1 baseline y=29.3 mm (21.3 pt), title2 baseline y=38.1 mm (17.8 pt)
    raw_name = normalize_event_name(str(p.get("event_name") or ""))
    parts = raw_name.split(" & ", 1)
    if len(parts) == 2:
        title1 = parts[0].strip()
        title2 = "& " + parts[1].strip()
    else:
        words = raw_name.split()
        mid   = max(1, (len(words) + 1) // 2)
        title1 = " ".join(words[:mid])
        title2 = " ".join(words[mid:])

    c.setFillColorRGB(0.969, 0.580, 0.114)          # ECSA orange
    c.setFont("Helvetica-Bold", 21)
    c.drawCentredString(W / 2, fy(29.3 + 21 * 25.4/72 * 0.75), title1)

    c.setFillColorRGB(0.06, 0.06, 0.06)             # near-black (matches official)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(W / 2, fy(38.1 + 18 * 25.4/72 * 0.75), title2)

    # ── Dates & location ──────────────────────────────────────────────────────
    # Extracted: date baseline y=46.1 mm, 11 pt
    dates    = str(p.get("event_dates") or "")
    loc      = str(p.get("location") or "")
    date_str = f"{dates}  |  {loc}" if (dates and loc) else (dates or loc)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    # Auto-size date string to fit within usable width (94 mm)
    for date_fs in (11, 9, 8, 7):
        c.setFont("Helvetica-Bold", date_fs)
        if c.stringWidth(date_str, "Helvetica-Bold", date_fs) <= 94 * mm:
            break
    c.drawCentredString(W / 2, fy(46.1 + date_fs * 25.4/72 * 0.75), date_str)

    # ── THEME box ─────────────────────────────────────────────────────────────
    # Extracted: rect (9.9, 53.9)→(28.1, 59.4) mm  |  label 12.6 pt
    c.setFillColorRGB(0.0, 0.681, 0.938)
    c.rect(9.9*mm, fy(59.4), 18.2*mm, 5.5*mm, fill=True, stroke=False)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 11)
    theme_box_cy = (53.9 + 59.4) / 2                # 56.65 mm from top
    c.drawCentredString(19.0*mm, fy(theme_box_cy + 11 * 25.4/72 * 0.3), "THEME:")

    # ── Theme text ────────────────────────────────────────────────────────────
    # Extracted: line1 y=60.7 mm, line2 y=64.6 mm  |  9 pt
    theme = str(p.get("event_theme") or "")
    c.setFillColorRGB(0.06, 0.06, 0.06)
    c.setFont("Helvetica-Bold", 8.5)
    if theme:
        limit = 55
        if len(theme) <= limit:
            c.drawString(10.2*mm, fy(60.7 + 8.5 * 25.4/72 * 0.75), theme)
        else:
            bp = theme.rfind(" ", 0, limit) or limit
            c.drawString(10.2*mm, fy(60.7 + 8.5 * 25.4/72 * 0.75), theme[:bp].rstrip())
            c.drawString(10.2*mm, fy(64.6 + 8.5 * 25.4/72 * 0.75), theme[bp:].strip())

    # ── Role banner ───────────────────────────────────────────────────────────
    # Extracted: rect (7.8, 74.0)→(97.9, 86.3) mm  |  text 30 pt
    c.setFillColorRGB(*role_rgb)
    c.rect(7.8*mm, fy(86.3), 90.1*mm, 12.3*mm, fill=True, stroke=False)

    fsize = max(22, min(42, int(330 // max(len(role_label), 1))))
    banner_cy = (74.0 + 86.3) / 2                   # 80.15 mm from top
    c.setFont("Helvetica-Bold", fsize)
    c.setFillColorRGB(*banner_txt)
    c.drawCentredString(W / 2, fy(banner_cy + fsize * 25.4/72 * 0.3), role_label)

    # ── Info rows: Name / Designation / Organization ──────────────────────────
    # Extracted box positions (mm from top):
    #   Name label     (7.8, 89.1)→(29.1, 95.8)  content (29.2, 89.1)→(97.8, 95.8)
    #   Designation    (7.8, 98.4)→(41.5, 105.0) content (41.2, 98.3)→(97.8, 105.0)
    #   Organization   (7.8, 107.6)→(41.9, 114.3)content (41.9, 107.7)→(97.8, 114.3)
    full_name = " ".join(filter(None, [
        str(p.get("title")       or "").strip(),
        str(p.get("firstname")   or "").strip(),
        str(p.get("lastname")    or "").strip(),
    ]))
    row_specs = [
        # (label, lbl_x0, lbl_x1, y0, y1, value)
        ("Name",         7.8, 29.1,  89.1,  95.8, full_name[:42]),
        ("Designation",  7.8, 41.5,  98.4, 105.0, str(p.get("position")     or "")[:38]),
        ("Organization", 7.8, 41.9, 107.6, 114.3, str(p.get("organisation") or "")[:38]),
    ]

    for lbl, lx0, lx1, y0f, y1f, val in row_specs:
        row_h_mm = y1f - y0f         # 6.6 mm
        rl_bot   = fy(y1f)
        lbl_w_mm = lx1 - lx0
        cont_w_mm = 97.8 - lx1
        row_cy   = (y0f + y1f) / 2

        # Label (darker cyan)
        c.setFillColorRGB(0.0, 0.681, 0.938)
        c.rect(lx0*mm, rl_bot, lbl_w_mm*mm, row_h_mm*mm, fill=True, stroke=False)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(((lx0 + lx1) / 2)*mm,
                            fy(row_cy + 11 * 25.4/72 * 0.3), lbl)

        # Content (light tint)
        c.setFillColorRGB(*role_light)
        c.rect(lx1*mm, rl_bot, cont_w_mm*mm, row_h_mm*mm, fill=True, stroke=False)
        c.setFillColorRGB(0.06, 0.06, 0.06)
        c.setFont("Helvetica-Bold", 10)
        c.drawString((lx1 + 1.5)*mm, fy(row_cy + 10 * 25.4/72 * 0.3), val)

    # ── QR code ───────────────────────────────────────────────────────────────
    # Fits between org row (114.3 mm) and flags (136 mm) → 18×18 mm centred
    qr_mm   = 18
    qr_top  = 115.5                  # mm from top
    qr_url  = (f"{CLIENT_ORIGIN}/event-attendance/{p['event_id']}"
               f"?reg={p['registration_id']}")
    try:
        qr_img = qrcode.make(qr_url)
        qr_buf = BytesIO()
        qr_img.save(qr_buf, format="PNG")
        qr_buf.seek(0)
        c.drawImage(ImageReader(qr_buf),
                    (W_mm - qr_mm) / 2 * mm, fy(qr_top + qr_mm),
                    qr_mm * mm, qr_mm * mm)
    except Exception:
        pass

    c.setFillColorRGB(0.4, 0.4, 0.4)
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(W / 2, fy(134.5), "Scan QR code to confirm attendance")

    # ── ECSA member-state flags ───────────────────────────────────────────────
    # Two rows at the very bottom (136–147 mm from top)
    flag_map   = _get_flag_images()
    all_flags  = [flag_map.get(code) for code in ECSA_FLAG_CODES]
    flag_w_mm  = 8.5
    flag_h_mm  = 5.5
    f_gap_mm   = 1.2
    flag_rows  = [all_flags[:5], all_flags[5:]]

    for ri, flag_row in enumerate(flag_rows):
        valid = [img for img in flag_row if img is not None]
        if not valid:
            continue
        n        = len(valid)
        row_w_mm = n * flag_w_mm + (n - 1) * f_gap_mm
        sx       = (W_mm - row_w_mm) / 2
        row_top  = 136.0 + ri * (flag_h_mm + f_gap_mm)
        flag_rl_y = fy(row_top + flag_h_mm)
        for j, img in enumerate(valid):
            try:
                c.drawImage(img,
                            (sx + j * (flag_w_mm + f_gap_mm)) * mm,
                            flag_rl_y,
                            flag_w_mm * mm, flag_h_mm * mm,
                            preserveAspectRatio=True)
            except Exception:
                pass

    c.showPage()


@router.get("/{event_id}/participants/badges")
async def download_participant_badges_pdf(
    request: Request,
    event_id: int,
    current_user: user_dependency,
    paid: Literal["all", "true", "false"] = Query("all"),
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    dependency=Depends(get_dependency),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    auth_dependency.secure_access("VIEW_EVENT", current_user["user_id"])
    client_ip = dependency.request_ip(request)
    dependency.log_activity(
        current_user["user_id"],
        "DOWNLOAD_BADGES",
        current_user["username"],
        client_ip,
        f"Downloaded participant badges for event {event_id} with filter paid={paid}",
    )

    event = get_object(event_id, db, Event)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    primary_color = (event.org_unit.primary_color or "#0095B6") if event.org_unit else "#0095B6"
    secondary_color = (event.org_unit.secondary_color or "#F7941D") if event.org_unit else "#F7941D"
    primary_rgb = hex_to_rgb(primary_color)
    secondary_rgb = hex_to_rgb(secondary_color)

    participants = []
    for reg in event.registrations:
        user = reg.user
        profile = user.user_profile[0] if user.user_profile else None
        country = profile.country.country if profile and profile.country else None
        organisation = profile.organisation if profile else None
        role_key = (
            reg.participation_role.name
            if hasattr(reg.participation_role, "name")
            else str(reg.participation_role).lower()
        )
        participants.append(
            {
                "registration_id": reg.id,
                "user_id": user.id,
                "event_id": event_id,
                "title": profile.title if profile else "",
                "firstname": user.firstname,
                "middle_name": profile.middle_name if profile else "",
                "lastname": user.lastname,
                "position": profile.position if profile else "",
                "organisation": organisation,
                "country": country,
                "participation_role": PARTICIPATION_ROLE_MAP.get(role_key, role_key),
                "event_name": event.event,
                "location": event.location or "",
                "event_theme": event.theme or "",
                "event_dates": _fmt_event_dates(event),
                "participation_role_raw": role_key,
                "paid": reg.paid,
            }
        )

    if paid != "all":
        is_paid = paid == "true"
        participants = [p for p in participants if p["paid"] == is_paid]

    # Optional single-participant filter (used by badge preview download button)
    if user_id is not None:
        participants = [p for p in participants if p.get("user_id") == user_id]

    if not participants:
        raise HTTPException(status_code=404, detail="No participants found")

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(105 * mm, 148 * mm))

    logo_left  = convert_png_to_rgb("assets/logo_left.png")
    logo_right = convert_png_to_rgb("assets/logo_right.png")

    for p in participants:
        _render_badge_page(c, p, logo_left, logo_right)

    c.save()
    buffer.seek(0)

    safe_event_name = sanitize_filename(event.event)
    ascii_filename = f"{safe_event_name}_participant_badges.pdf"
    utf8_filename = urllib.parse.quote(ascii_filename)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={ascii_filename}; filename*=UTF-8''{utf8_filename}"
        },
    )


@router.get("/{event_id}/my-badge")
async def download_my_badge(
    event_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
):
    """Generate a badge PDF for the currently authenticated paid user."""
    event = get_object(event_id, db, Event)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    reg = db.query(Registration).filter(
        Registration.user_id == current_user["user_id"],
        Registration.event_id == event_id,
        Registration.deleted_at == None,
    ).first()

    if not reg:
        raise HTTPException(status_code=404, detail="You are not registered for this event")
    if not reg.paid:
        raise HTTPException(status_code=403, detail="Badge is only available after payment is confirmed")

    user = reg.user
    profile = user.user_profile[0] if user.user_profile else None
    country = profile.country.country if profile and profile.country else None
    organisation = profile.organisation if profile else None
    role_key = (
        reg.participation_role.name
        if hasattr(reg.participation_role, "name")
        else str(reg.participation_role).lower()
    )

    primary_color = (event.org_unit.primary_color or "#0095B6") if event.org_unit else "#0095B6"
    secondary_color = (event.org_unit.secondary_color or "#F7941D") if event.org_unit else "#F7941D"
    primary_rgb = hex_to_rgb(primary_color)
    secondary_rgb = hex_to_rgb(secondary_color)

    p = {
        "registration_id": reg.id,
        "event_id": event_id,
        "title": profile.title if profile else "",
        "firstname": user.firstname,
        "middle_name": profile.middle_name if profile else "",
        "lastname": user.lastname,
        "position": profile.position if profile else "",
        "organisation": organisation,
        "country": country,
        "participation_role": PARTICIPATION_ROLE_MAP.get(role_key, role_key),
        "event_name": event.event,
        "location": event.location or "",
        "event_theme": event.theme or "",
        "event_dates": _fmt_event_dates(event),
        "participation_role_raw": role_key,
        "paid": reg.paid,
    }

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(105 * mm, 148 * mm))

    logo_left  = convert_png_to_rgb("assets/logo_left.png")
    logo_right = convert_png_to_rgb("assets/logo_right.png")

    _render_badge_page(c, p, logo_left, logo_right)

    c.save()
    buffer.seek(0)

    safe_name = sanitize_filename(f"{user.firstname}_{user.lastname}")
    ascii_filename = f"badge_{safe_name}.pdf"
    utf8_filename = urllib.parse.quote(ascii_filename)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={ascii_filename}; filename*=UTF-8''{utf8_filename}"
        },
    )


@router.get("/{event_id}/attendance")
async def get_event_attendance(
    event_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    """Admin: get all attendance records for an event."""
    auth_dependency.secure_access("VIEW_EVENT", current_user["user_id"])

    from models.models import EventAttendance
    records = (
        db.query(EventAttendance)
        .join(Registration, EventAttendance.registration_id == Registration.id)
        .filter(Registration.event_id == event_id)
        .order_by(EventAttendance.attendance_date.desc())
        .all()
    )

    result = []
    for a in records:
        reg = a.registration
        user = reg.user if reg else None
        profile = user.user_profile[0] if user and user.user_profile else None
        result.append({
            "id": a.id,
            "registration_id": a.registration_id,
            "attendance_date": a.attendance_date,
            "firstname": user.firstname if user else "",
            "lastname": user.lastname if user else "",
            "email": user.email if user else "",
            "organisation": profile.organisation if profile else "",
            "country": profile.country.country if profile and profile.country else "",
            "participation_role": reg.participation_role.name if reg else "",
            "paid": reg.paid if reg else False,
        })

    return {"total": len(result), "data": result}


@router.delete("/{event_id}/attendance")
async def reset_event_attendance(
    event_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    """Admin: delete all attendance records for an event."""
    auth_dependency.secure_access("VIEW_EVENT", current_user["user_id"])

    from models.models import EventAttendance
    records = (
        db.query(EventAttendance)
        .join(Registration, EventAttendance.registration_id == Registration.id)
        .filter(Registration.event_id == event_id)
        .all()
    )
    count = len(records)
    for r in records:
        db.delete(r)
    db.commit()
    return {"detail": f"Deleted {count} attendance record(s)"}


@router.get("/{event_id}/attendance/export")
async def export_event_attendance(
    event_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    """Admin: export attendance records as Excel."""
    auth_dependency.secure_access("VIEW_EVENT", current_user["user_id"])

    from models.models import EventAttendance
    from io import BytesIO
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment
    from fastapi.responses import StreamingResponse

    records = (
        db.query(EventAttendance)
        .join(Registration, EventAttendance.registration_id == Registration.id)
        .filter(Registration.event_id == event_id)
        .order_by(EventAttendance.attendance_date.asc())
        .all()
    )

    event = db.query(Event).filter(Event.id == event_id).first()
    event_name = event.event if event else f"Event {event_id}"

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Attendance"

    headers = ["#", "First Name", "Last Name", "Email", "Organisation", "Country", "Role", "Check-in Time", "Payment"]
    header_fill = PatternFill("solid", fgColor="1B3F6E")
    header_font = Font(bold=True, color="FFFFFF")
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

    for i, a in enumerate(records, 1):
        reg = a.registration
        user = reg.user if reg else None
        profile = user.user_profile[0] if user and user.user_profile else None
        checkin = a.attendance_date
        checkin_str = checkin.strftime("%Y-%m-%d %H:%M") if checkin else ""
        ws.append([
            i,
            user.firstname if user else "",
            user.lastname if user else "",
            user.email if user else "",
            profile.organisation if profile else "",
            profile.country.country if profile and profile.country else "",
            reg.participation_role.name if reg else "",
            checkin_str,
            "Paid" if (reg.paid if reg else False) else "Unpaid",
        ])

    col_widths = [4, 16, 16, 28, 26, 18, 16, 20, 10]
    for col, width in enumerate(col_widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = width

    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)

    safe_name = "".join(c if c.isalnum() or c in "-_ " else "_" for c in event_name)[:40]
    filename = f"attendance_{safe_name}.xlsx"
    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


class PaymentReminderSchema(BaseModel):
    registration_ids: list[int] = []  # empty = send to ALL unpaid

@router.post("/{event_id}/send-payment-reminders")
async def send_payment_reminders(
    event_id: int,
    background_tasks: BackgroundTasks,
    current_user: user_dependency,
    body: PaymentReminderSchema = PaymentReminderSchema(),
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    """Admin: send payment reminder emails to selected (or all) unpaid registrants."""
    auth_dependency.secure_access("VIEW_EVENT", current_user["user_id"])

    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    q = (
        db.query(Registration)
        .join(User, Registration.user_id == User.id)
        .filter(
            Registration.event_id == event_id,
            Registration.paid == False,
            Registration.deleted_at == None,
            User.deleted_at == None,
        )
        .options(joinedload(Registration.user))
    )

    if body.registration_ids:
        q = q.filter(Registration.id.in_(body.registration_ids))

    targets = q.all()

    if not targets:
        return {"sent": 0, "message": "No matching unpaid registrations found."}

    import utils.mailer_util as mailer_util
    now = datetime.utcnow()
    for reg in targets:
        user = reg.user
        if user and user.email:
            mailer_util.payment_reminder_email(
                recipient_email=user.email,
                firstname=user.firstname or "Participant",
                event_name=event.event,
                payment_url="https://ecsahc.org/payment/",
                portal_url="https://events.ecsahc.org",
                background_tasks=background_tasks,
                db=db,
                sent_by_user_id=current_user["user_id"],
            )
            reg.reminder_sent_at = now

    db.commit()

    return {
        "sent": len(targets),
        "message": f"Payment reminder sent to {len(targets)} participant(s).",
    }


@router.post("/{event_id}/send-pending-reminder/{registration_id}")
async def send_single_pending_reminder(
    event_id: int,
    registration_id: int,
    background_tasks: BackgroundTasks,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    """Admin: send a payment reminder to a single pending registration."""
    auth_dependency.secure_access("ADMIN_DASHBOARD", current_user["user_id"])

    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    registration = db.query(Registration).filter(
        Registration.id == registration_id,
        Registration.event_id == event_id,
        Registration.deleted_at == None,
    ).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    import utils.mailer_util as mailer_util
    payment_url = f"https://events.ecsahc.org/payment/{event_id}/{registration_id}"
    if registration.user and registration.user.email:
        mailer_util.payment_reminder_email(
            recipient_email=registration.user.email,
            firstname=registration.user.firstname or "Participant",
            event_name=event.event,
            payment_url=payment_url,
            portal_url="https://events.ecsahc.org",
            background_tasks=background_tasks,
            db=db,
            sent_by_user_id=current_user["user_id"],
        )

    return {"message": "Reminder sent successfully."}


@router.post("/{event_id}/send-pending-bulk-reminders")
async def send_pending_bulk_reminders(
    event_id: int,
    background_tasks: BackgroundTasks,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    """Admin: send payment reminders to all pending (no proof uploaded) registrations."""
    auth_dependency.secure_access("ADMIN_DASHBOARD", current_user["user_id"])

    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    all_targets = (
        db.query(Registration)
        .filter(
            Registration.event_id == event_id,
            Registration.paid == False,
            Registration.payment_proof == None,
            Registration.deleted_at == None,
        )
        .all()
    )

    # Exclude accepted abstract authors — they get their own reminder from the abstracts page
    from sqlalchemy import text as _sql_text
    _author_rows = db.execute(_sql_text(
        "SELECT DISTINCT LOWER(aa.email) as email FROM abstract a "
        "JOIN abstract_author aa ON aa.abstract_id = a.id "
        "WHERE a.event_id = :eid AND a.status = 'accepted' AND aa.email IS NOT NULL"
    ), {"eid": event_id}).fetchall()
    excluded_emails = {row.email for row in _author_rows}

    targets = [
        t for t in all_targets
        if t.user and t.user.email and t.user.email.lower() not in excluded_emails
    ]

    if not targets:
        return {"sent": 0, "message": "No pending registrations found (abstract authors are excluded)."}

    import utils.mailer_util as mailer_util
    for reg in targets:
        if reg.user and reg.user.email:
            payment_url = f"https://events.ecsahc.org/payment/{event_id}/{reg.id}"
            mailer_util.payment_reminder_email(
                recipient_email=reg.user.email,
                firstname=reg.user.firstname or "Participant",
                event_name=event.event,
                payment_url=payment_url,
                portal_url="https://events.ecsahc.org",
                background_tasks=background_tasks,
                db=db,
                sent_by_user_id=current_user["user_id"],
            )

    return {
        "sent": len(targets),
        "excluded_abstract_authors": len(excluded_emails),
        "message": f"Payment reminder sent to {len(targets)} pending registration(s). {len(excluded_emails)} abstract author(s) excluded.",
    }


# ── Admin: look up user by email ──────────────────────────────────────────────
@router.get("/{event_id}/lookup-user")
async def lookup_user_by_email(
    event_id: int,
    email: str = Query(...),
    current_user: user_dependency = None,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    """Look up whether a user with the given email already exists."""
    auth_dependency.secure_access("ADMIN_DASHBOARD", current_user["user_id"])
    user = db.query(User).filter(User.email == email, User.deleted_at == None).first()
    if not user:
        return {"exists": False}

    # Check if already registered for this event
    reg = db.query(Registration).filter(
        Registration.user_id == user.id,
        Registration.event_id == event_id,
        Registration.deleted_at == None,
    ).first()

    return {
        "exists": True,
        "user_id": user.id,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
        "already_registered": bool(reg),
        "current_role": reg.participation_role.name if reg else None,
    }


# ── Admin: add (or re-register) a participant to an event ────────────────────
class AdminAddParticipantSchema(BaseModel):
    email: str
    firstname: str = ""
    lastname: str = ""
    participation_role: str
    send_invitation: bool = True
    payment_url: str = "https://ecsahc.org/payment/"
    portal_url: str = "https://events.ecsahc.org"


@router.post("/{event_id}/admin-add-participant")
async def admin_add_participant(
    event_id: int,
    body: AdminAddParticipantSchema,
    background_tasks: BackgroundTasks,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dependency),
):
    """Admin: find-or-create a user, register them to the event, optionally send invitation."""
    auth_dependency.secure_access("ADMIN_DASHBOARD", current_user["user_id"])

    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Validate role
    try:
        role_enum = ParticipationRole[body.participation_role]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid participation role: {body.participation_role}")

    # ── 1. Find or create the user ────────────────────────────────────────────
    is_new_user = False
    temp_password = None

    user = db.query(User).filter(User.email == body.email, User.deleted_at == None).first()

    if not user:
        # Create new user with a temp password
        if not body.firstname or not body.lastname:
            raise HTTPException(
                status_code=400,
                detail="First name and last name are required for new users."
            )
        from passlib.hash import bcrypt as bcrypt_hash
        temp_password = auth_dependency.generate_random_password()
        hashed = bcrypt_hash.hash(temp_password)
        user = User(
            firstname=body.firstname,
            lastname=body.lastname,
            email=body.email,
            phone="",
            hashed_password=hashed,
            verified=1,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        is_new_user = True
    else:
        # Update name if the admin supplied different values
        changed = False
        if body.firstname and body.firstname != user.firstname:
            user.firstname = body.firstname
            changed = True
        if body.lastname and body.lastname != user.lastname:
            user.lastname = body.lastname
            changed = True
        if changed:
            db.commit()

    # ── 2. Register (or update role if already registered) ────────────────────
    # Roles that are exempt from payment — mark as paid automatically
    NO_PAYMENT_ROLES = {"secretariat"}
    auto_paid = body.participation_role in NO_PAYMENT_ROLES

    existing_reg = db.query(Registration).filter(
        Registration.user_id == user.id,
        Registration.event_id == event_id,
        Registration.deleted_at == None,
    ).first()

    if existing_reg:
        existing_reg.participation_role = role_enum
        if auto_paid:
            existing_reg.paid = True
        db.commit()
        db.refresh(existing_reg)
        reg_id = existing_reg.id
        action = "updated"
    else:
        new_reg = Registration(
            user_id=user.id,
            event_id=event_id,
            participation_role=role_enum,
            paid=auto_paid,
        )
        db.add(new_reg)
        db.commit()
        db.refresh(new_reg)
        reg_id = new_reg.id
        action = "registered"

    # ── 3. Send email ─────────────────────────────────────────────────────────
    import utils.mailer_util as mailer_util

    # Build friendly role label
    role_labels = {
        "secretariat": "ECSA-HC Secretariat",
        "moh": "Country Delegate (Ministry of Health)",
        "member_state": "Participant from ECSA Member States",
        "other_africa": "Participant from other African countries",
        "world": "International Participant",
        "student": "Student",
        "exhibitor": "Sponsor / Exhibitor",
        "participant": "Participant",
        "delegate": "Delegate",
        "presenter": "Presenter",
        "speaker": "Speaker",
        "sponsor": "Sponsor",
        "moderator": "Moderator",
    }
    role_label = role_labels.get(body.participation_role, body.participation_role)

    # Format event dates
    event_dates = None
    if event.start_date and event.end_date:
        def _fmt(d):
            return d.strftime("%-d %B %Y") if hasattr(d, "strftime") else str(d)
        event_dates = f"{_fmt(event.start_date)} – {_fmt(event.end_date)}"

    email_sent = False

    if is_new_user:
        # Brand-new user created inline: send welcome + event invitation with credentials
        mailer_util.event_invitation_email(
            recipient_email=user.email,
            firstname=user.firstname,
            event_name=event.event,
            participation_role=role_label,
            event_location=event.location,
            event_dates=event_dates,
            is_new_user=True,
            password=temp_password,
            no_payment=auto_paid,
            portal_url=body.portal_url,
            payment_url=body.payment_url,
            background_tasks=background_tasks,
            db=db,
            sent_by_user_id=current_user["user_id"],
        )
        user.credentials_sent = True
        db.commit()
        email_sent = True

    elif body.send_invitation:
        if not user.credentials_sent:
            # Existing user who has never received their credentials yet
            # (created silently via User Management). Issue a fresh password
            # so we can include it in the invitation.
            from passlib.hash import bcrypt as bcrypt_hash
            fresh_password = auth_dependency.generate_random_password()
            user.hashed_password = bcrypt_hash.hash(fresh_password)
            user.credentials_sent = True
            db.commit()
            db.refresh(user)
            mailer_util.event_invitation_email(
                recipient_email=user.email,
                firstname=user.firstname,
                event_name=event.event,
                participation_role=role_label,
                event_location=event.location,
                event_dates=event_dates,
                is_new_user=True,
                password=fresh_password,
                no_payment=auto_paid,
                portal_url=body.portal_url,
                payment_url=body.payment_url,
                background_tasks=background_tasks,
                db=db,
                sent_by_user_id=current_user["user_id"],
            )
        else:
            # Existing user who already has their credentials: send event-only invitation
            mailer_util.event_invitation_email(
                recipient_email=user.email,
                firstname=user.firstname,
                event_name=event.event,
                participation_role=role_label,
                event_location=event.location,
                event_dates=event_dates,
                is_new_user=False,
                password=None,
                no_payment=auto_paid,
                portal_url=body.portal_url,
                payment_url=body.payment_url,
                background_tasks=background_tasks,
                db=db,
                sent_by_user_id=current_user["user_id"],
            )
        email_sent = True

    return {
        "user_id": user.id,
        "registration_id": reg_id,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
        "is_new_user": is_new_user,
        "action": action,
        "email_sent": email_sent,
        "message": (
            f"{'New user created and registered' if is_new_user else f'Existing user {action}'}"
            f" to {event.event}."
            f"{' Invitation email sent.' if email_sent else ''}"
        ),
    }


# ══════════════════════════════════════════════════════════════════════════════
#  EVENT TEMPLATES  (PPT / poster templates downloadable by accepted+paid users)
# ══════════════════════════════════════════════════════════════════════════════

TEMPLATE_DIR = "uploads/templates"
if not os.path.exists(TEMPLATE_DIR):
    os.makedirs(TEMPLATE_DIR)


@router.post("/templates/upload", status_code=201)
async def upload_event_template(
    file: UploadFile = File(...),
    event_id: int = Form(None),
    name: str = Form(...),
    presentation_type: str = Form(None),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(lambda db=Depends(get_db): Auth(db)),
):
    auth_dependency.secure_access("VIEW_ABSTRACTS", current_user["user_id"])
    from models.models import EventTemplate
    ext = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(TEMPLATE_DIR, unique_name)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    t = EventTemplate(
        event_id=event_id or None,
        name=name,
        file_path=file_path,
        presentation_type=presentation_type or None,
        uploaded_by=current_user["user_id"],
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return _serialize_template(t)


@router.get("/templates")
def list_templates(
    event_id: int = Query(None),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(lambda db=Depends(get_db): Auth(db)),
):
    auth_dependency.secure_access("VIEW_ABSTRACTS", current_user["user_id"])
    from models.models import EventTemplate
    q = db.query(EventTemplate)
    if event_id:
        q = q.filter(
            (EventTemplate.event_id == event_id) | (EventTemplate.event_id == None)
        )
    return [_serialize_template(t) for t in q.order_by(EventTemplate.uploaded_at.desc()).all()]


@router.delete("/templates/{template_id}", status_code=204)
def delete_template(
    template_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(lambda db=Depends(get_db): Auth(db)),
):
    auth_dependency.secure_access("VIEW_ABSTRACTS", current_user["user_id"])
    from models.models import EventTemplate
    t = db.query(EventTemplate).filter(EventTemplate.id == template_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Template not found")
    if os.path.exists(t.file_path):
        os.remove(t.file_path)
    db.delete(t)
    db.commit()


@router.get("/templates/for-me")
def my_templates(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return templates accessible to this user (accepted abstract + paid registration)."""
    from models.models import EventTemplate, Abstract, AbstractStatus, Registration
    user_id = current_user["user_id"]

    # Find event IDs where user has a paid registration
    paid_event_ids = {
        r.event_id for r in
        db.query(Registration).filter(
            Registration.user_id == user_id, Registration.paid == True
        ).all()
    }

    # Find event IDs where user has an accepted abstract (submitted_by OR as author)
    from models.models import AbstractAuthor
    from sqlalchemy import or_
    accepted_abstracts = db.query(Abstract).filter(
        Abstract.status == AbstractStatus.accepted,
        Abstract.deleted_at == None,
        or_(
            Abstract.submitted_by == user_id,
            Abstract.id.in_(
                db.query(AbstractAuthor.abstract_id)
                .join(User, User.email == AbstractAuthor.email)
                .filter(User.id == user_id)
            )
        )
    ).all()
    accepted_event_ids = {a.event_id for a in accepted_abstracts}

    # Eligible = paid AND accepted
    eligible_event_ids = paid_event_ids & accepted_event_ids

    if not eligible_event_ids:
        return []

    from models.models import EventTemplate
    templates = db.query(EventTemplate).filter(
        (EventTemplate.event_id.in_(eligible_event_ids)) |
        (EventTemplate.event_id == None)
    ).order_by(EventTemplate.uploaded_at.desc()).all()

    # Also attach presentation_type from the user's abstract
    abs_type_by_event = {}
    for a in accepted_abstracts:
        abs_type_by_event[a.event_id] = a.presentation_type.value if a.presentation_type else None

    result = []
    for t in templates:
        p_type = abs_type_by_event.get(t.event_id) if t.event_id else None
        # Only show template if ptype matches user's abstract type (or template has no type restriction)
        if t.presentation_type and p_type and t.presentation_type != p_type:
            continue
        result.append(_serialize_template(t))
    return result


def _serialize_template(t):
    from models.models import Event as _Event
    return {
        "id": t.id,
        "event_id": t.event_id,
        "name": t.name,
        "file_path": t.file_path,
        "url": f"/uploads/templates/{os.path.basename(t.file_path)}",
        "presentation_type": t.presentation_type,
        "uploaded_at": t.uploaded_at,
    }
