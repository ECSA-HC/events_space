import io
from typing import Annotated, Optional
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

from core.database import get_db
from dependencies.auth_dependency import Auth, get_current_user, get_optional_current_user
from dependencies.dependency import Dependency
import utils.mailer_util as mailer_util
from models.models import Abstract, AbstractAuthor, AbstractReviewer, AbstractReview, User, UserRole, Role, EventTrack
from datetime import datetime
from schemas.events_space import (
    AbstractSubmitSchema, AbstractUpdateSchema,
    AssignReviewerSchema, BulkAssignReviewerSchema, AbstractReviewSchema,
    CreateReviewerSchema,
)

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


def get_auth_dep(db: Session = Depends(get_db)) -> Auth:
    return Auth(db)


def get_dependency(db: Session = Depends(get_db)) -> Dependency:
    return Dependency(db)


def _serialize_abstract(a: Abstract):
    return {
        "id": a.id,
        "event_id": a.event_id,
        "event": a.event.event if a.event else None,
        "title": a.title,
        "abstract_text": a.abstract_text,
        "keywords": a.keywords,
        "track": a.track,
        "track_id": a.track_id,
        "track_code": a.event_track.code if a.event_track else None,
        "track_title": a.event_track.title if a.event_track else None,
        "track_theme": a.event_track.theme if a.event_track else None,
        "presentation_type": a.presentation_type.value if a.presentation_type else None,
        "status": a.status.value if a.status else None,
        "word_count": a.word_count,
        "submitted_by": a.submitted_by,
        "submitter_name": f"{a.submitter.firstname} {a.submitter.lastname}" if a.submitter else (f"{a.authors[0].firstname} {a.authors[0].lastname}" if a.authors else None),
        "submitter_email": a.submitter.email if a.submitter else (a.authors[0].email if a.authors else None),
        "created_at": a.created_at,
        "updated_at": a.updated_at,
        "authors": [
            {
                "id": au.id,
                "firstname": au.firstname,
                "lastname": au.lastname,
                "email": au.email,
                "affiliation": au.affiliation,
                "country": au.country,
                "is_presenting": au.is_presenting,
                "author_order": au.author_order,
            }
            for au in a.authors
        ],
        "reviewer_assignments": [
            {
                "id": ra.id,
                "reviewer_id": ra.reviewer_id,
                "reviewer_name": f"{ra.reviewer.firstname} {ra.reviewer.lastname}" if ra.reviewer else None,
                "reviewer_email": ra.reviewer.email if ra.reviewer else None,
                "assigned_at": ra.assigned_at,
                "completed": ra.completed,
                "review": {
                    "id": ra.review.id,
                    "relevance_score": ra.review.relevance_score,
                    "methodology_score": ra.review.methodology_score,
                    "originality_score": ra.review.originality_score,
                    "overall_score": ra.review.overall_score,
                    "recommendation": ra.review.recommendation.value,
                    "comments": ra.review.comments,
                    "submitted_at": ra.review.submitted_at,
                } if ra.review else None,
            }
            for ra in a.reviewer_assignments
        ],
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
def submit_abstract(
    request: Request,
    schema: AbstractSubmitSchema,
    current_user: Optional[dict] = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
    dependency: Dependency = Depends(get_dependency),
):
    word_count = len(schema.abstract_text.split())

    # Resolve track text from track_id if provided
    track_text = schema.track
    track_id   = schema.track_id
    if track_id:
        track_record = db.query(EventTrack).filter(EventTrack.id == track_id).first()
        if track_record:
            track_text = f"{track_record.code}: {track_record.title}"
        else:
            track_id = None

    # Determine the submitter: logged-in user takes priority.
    # For anonymous submissions, link to an existing account if the email matches.
    # Account creation is deferred to the conference registration step.
    submitter_id = current_user["user_id"] if current_user else None
    submitter_email = current_user["username"] if current_user else None

    if not submitter_id and schema.authors:
        first_author = schema.authors[0]
        if first_author.email:
            existing = db.query(User).filter(
                User.email == first_author.email,
                User.deleted_at == None,
            ).first()
            if existing:
                submitter_id = existing.id
                submitter_email = existing.email

    abstract = Abstract(
        event_id=schema.event_id,
        submitted_by=submitter_id,
        title=schema.title,
        abstract_text=schema.abstract_text,
        keywords=schema.keywords,
        track=track_text,
        track_id=track_id,
        presentation_type=schema.presentation_type,
        word_count=word_count,
    )
    db.add(abstract)
    db.flush()

    for i, author in enumerate(schema.authors):
        db.add(AbstractAuthor(
            abstract_id=abstract.id,
            firstname=author.firstname,
            lastname=author.lastname,
            email=author.email,
            affiliation=author.affiliation,
            country=author.country,
            is_presenting=author.is_presenting,
            author_order=i,
        ))

    db.commit()
    db.refresh(abstract)
    abstract = db.query(Abstract).options(
        joinedload(Abstract.authors),
        joinedload(Abstract.submitter),
        joinedload(Abstract.event),
        joinedload(Abstract.event_track),
        joinedload(Abstract.reviewer_assignments),
    ).filter(Abstract.id == abstract.id).first()

    if submitter_id and submitter_email:
        dependency.log_activity(
            submitter_id,
            "SUBMIT_ABSTRACT",
            submitter_email,
            dependency.request_ip(request),
            f"Submitted abstract: {schema.title}",
        )

    first_author = schema.authors[0] if schema.authors else None
    return {
        "abstract": _serialize_abstract(abstract),
        "abstract_id": abstract.id,
        "author_firstname": first_author.firstname if first_author else None,
        "author_lastname": first_author.lastname if first_author else None,
        "author_email": first_author.email if first_author else None,
    }


@router.get("/")
def list_abstracts(
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dep),
    event_id: int = None,
    skip: int = 0,
    limit: int = 100,
):
    auth_dependency.secure_access("VIEW_ABSTRACTS", current_user["user_id"])
    q = db.query(Abstract).options(
        joinedload(Abstract.authors),
        joinedload(Abstract.submitter),
        joinedload(Abstract.event),
        joinedload(Abstract.event_track),
        joinedload(Abstract.reviewer_assignments).joinedload(AbstractReviewer.reviewer),
        joinedload(Abstract.reviewer_assignments).joinedload(AbstractReviewer.review),
    ).filter(Abstract.deleted_at == None)
    if event_id:
        q = q.filter(Abstract.event_id == event_id)
    abstracts = q.order_by(Abstract.created_at.desc()).offset(skip).limit(limit).all()
    return [_serialize_abstract(a) for a in abstracts]


@router.get("/export")
def export_abstracts(
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dep),
    event_id: int = None,
    status_filter: str = Query(None, alias="status"),
    search: str = Query(None),
):
    auth_dependency.secure_access("EXPORT_ABSTRACTS", current_user["user_id"])
    from sqlalchemy import or_
    q = db.query(Abstract).options(
        joinedload(Abstract.authors),
        joinedload(Abstract.submitter),
        joinedload(Abstract.event),
        joinedload(Abstract.reviewer_assignments).joinedload(AbstractReviewer.reviewer),
        joinedload(Abstract.reviewer_assignments).joinedload(AbstractReviewer.review),
    ).filter(Abstract.deleted_at == None)
    if event_id:
        q = q.filter(Abstract.event_id == event_id)
    if status_filter:
        q = q.filter(Abstract.status == status_filter)
    if search:
        term = f"%{search}%"
        q = q.filter(or_(
            Abstract.title.ilike(term),
            Abstract.keywords.ilike(term),
        ))
    abstracts = q.order_by(Abstract.created_at.desc()).all()

    wb = Workbook()

    # ── Sheet 1: Abstracts ────────────────────────────────────────────────────
    ws = wb.active
    ws.title = "Abstracts"

    header_fill = PatternFill("solid", start_color="0095B6")
    alt_fill    = PatternFill("solid", start_color="E8F4F8")
    header_font = Font(name="Arial", bold=True, color="FFFFFF", size=10)
    body_font   = Font(name="Arial", size=10)
    center      = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left        = Alignment(horizontal="left",   vertical="center", wrap_text=True)

    headers = [
        "#", "Title", "Event", "Track", "Presentation Type", "Status",
        "Word Count", "Keywords", "Submitter Name", "Submitter Email",
        "First Author", "First Author Email", "First Author Affiliation",
        "First Author Country", "All Authors", "Reviewers Assigned",
        "Reviews Completed", "Avg Relevance", "Avg Methodology",
        "Avg Originality", "Avg Overall", "Date Submitted",
    ]

    ws.row_dimensions[1].height = 22
    for ci, h in enumerate(headers, 1):
        cell = ws.cell(1, ci, h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center

    ws.freeze_panes = "A2"

    for ri, a in enumerate(abstracts, 2):
        ws.row_dimensions[ri].height = 16
        use_fill = alt_fill if ri % 2 == 0 else PatternFill("solid", start_color="FFFFFF")

        authors = sorted(a.authors, key=lambda x: x.author_order)
        first   = authors[0] if authors else None
        all_authors = "; ".join(
            f"{au.firstname} {au.lastname}" + (f" ({au.affiliation})" if au.affiliation else "")
            for au in authors
        )

        assignments = a.reviewer_assignments
        reviews = [r.review for r in assignments if r.review]
        avg = lambda field: round(sum(getattr(r, field) for r in reviews) / len(reviews), 1) if reviews else ""

        row = [
            a.id,
            a.title,
            a.event.event if a.event else "",
            a.track or "",
            a.presentation_type.value if a.presentation_type else "",
            a.status.value.replace("_", " ").title() if a.status else "",
            a.word_count or 0,
            a.keywords or "",
            f"{a.submitter.firstname} {a.submitter.lastname}" if a.submitter else "",
            a.submitter.email if a.submitter else "",
            f"{first.firstname} {first.lastname}" if first else "",
            first.email or "" if first else "",
            first.affiliation or "" if first else "",
            first.country or "" if first else "",
            all_authors,
            len(assignments),
            len(reviews),
            avg("relevance_score"),
            avg("methodology_score"),
            avg("originality_score"),
            avg("overall_score"),
            a.created_at.strftime("%d %b %Y") if a.created_at else "",
        ]

        for ci, val in enumerate(row, 1):
            cell = ws.cell(ri, ci, val)
            cell.font = body_font
            cell.fill = use_fill
            cell.alignment = left

    # Auto column widths
    col_widths = [6, 40, 30, 20, 16, 16, 10, 30, 22, 28, 22, 28, 28, 16, 50, 10, 10, 12, 12, 12, 12, 14]
    for ci, w in enumerate(col_widths, 1):
        ws.column_dimensions[get_column_letter(ci)].width = w

    # ── Sheet 2: Authors ──────────────────────────────────────────────────────
    ws2 = wb.create_sheet("Authors")
    ws2.sheet_properties.tabColor = "0095B6"
    auth_headers = ["Abstract #", "Abstract Title", "Author Order", "First Name", "Last Name",
                    "Email", "Affiliation", "Country", "Is Presenting"]
    ws2.row_dimensions[1].height = 22
    for ci, h in enumerate(auth_headers, 1):
        cell = ws2.cell(1, ci, h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center
    ws2.freeze_panes = "A2"
    ri2 = 2
    for a in abstracts:
        for au in sorted(a.authors, key=lambda x: x.author_order):
            use_fill = alt_fill if ri2 % 2 == 0 else PatternFill("solid", start_color="FFFFFF")
            row = [a.id, a.title, au.author_order + 1, au.firstname, au.lastname,
                   au.email or "", au.affiliation or "", au.country or "",
                   "Yes" if au.is_presenting else "No"]
            for ci, val in enumerate(row, 1):
                cell = ws2.cell(ri2, ci, val)
                cell.font = body_font
                cell.fill = use_fill
                cell.alignment = left
            ri2 += 1
    for ci, w in enumerate([10, 40, 12, 16, 16, 28, 28, 16, 12], 1):
        ws2.column_dimensions[get_column_letter(ci)].width = w

    # ── Sheet 3: Reviews ──────────────────────────────────────────────────────
    ws3 = wb.create_sheet("Reviews")
    ws3.sheet_properties.tabColor = "0095B6"
    rev_headers = ["Abstract #", "Abstract Title", "Reviewer Name", "Reviewer Email",
                   "Completed", "Relevance", "Methodology", "Originality",
                   "Overall", "Recommendation", "Comments", "Review Date"]
    ws3.row_dimensions[1].height = 22
    for ci, h in enumerate(rev_headers, 1):
        cell = ws3.cell(1, ci, h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center
    ws3.freeze_panes = "A2"
    ri3 = 2
    for a in abstracts:
        for ra in a.reviewer_assignments:
            use_fill = alt_fill if ri3 % 2 == 0 else PatternFill("solid", start_color="FFFFFF")
            rv = ra.review
            row = [
                a.id, a.title,
                f"{ra.reviewer.firstname} {ra.reviewer.lastname}" if ra.reviewer else "",
                ra.reviewer.email if ra.reviewer else "",
                "Yes" if ra.completed else "No",
                rv.relevance_score if rv else "",
                rv.methodology_score if rv else "",
                rv.originality_score if rv else "",
                rv.overall_score if rv else "",
                rv.recommendation.value.replace("_", " ").title() if rv else "",
                rv.comments if rv else "",
                rv.submitted_at.strftime("%d %b %Y") if rv and rv.submitted_at else "",
            ]
            for ci, val in enumerate(row, 1):
                cell = ws3.cell(ri3, ci, val)
                cell.font = body_font
                cell.fill = use_fill
                cell.alignment = left
            ri3 += 1
    for ci, w in enumerate([10, 40, 22, 28, 10, 10, 12, 12, 10, 18, 50, 12], 1):
        ws3.column_dimensions[get_column_letter(ci)].width = w

    # Style sheet tabs
    ws.sheet_properties.tabColor = "0095B6"

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)

    filename = "abstracts_export.xlsx"
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/my-submissions")
def my_submissions(
    current_user: user_dependency,
    db: Session = Depends(get_db),
):
    abstracts = db.query(Abstract).options(
        joinedload(Abstract.authors),
        joinedload(Abstract.event),
        joinedload(Abstract.reviewer_assignments),
    ).filter(
        Abstract.submitted_by == current_user["user_id"],
        Abstract.deleted_at == None,
    ).order_by(Abstract.created_at.desc()).all()
    return [_serialize_abstract(a) for a in abstracts]


@router.get("/my-reviews")
def my_reviews(
    current_user: user_dependency,
    db: Session = Depends(get_db),
):
    assignments = db.query(AbstractReviewer).options(
        joinedload(AbstractReviewer.abstract).joinedload(Abstract.authors),
        joinedload(AbstractReviewer.abstract).joinedload(Abstract.event),
        joinedload(AbstractReviewer.review),
    ).filter(
        AbstractReviewer.reviewer_id == current_user["user_id"],
    ).all()
    return [
        {
            "assignment_id": a.id,
            "assigned_at": a.assigned_at,
            "completed": a.completed,
            "abstract": _serialize_abstract(a.abstract),
            "review": {
                "id": a.review.id,
                "relevance_score": a.review.relevance_score,
                "methodology_score": a.review.methodology_score,
                "originality_score": a.review.originality_score,
                "overall_score": a.review.overall_score,
                "recommendation": a.review.recommendation.value,
                "comments": a.review.comments,
                "submitted_at": a.review.submitted_at,
            } if a.review else None,
        }
        for a in assignments
    ]


@router.get("/reviewers/candidates")
def list_reviewer_candidates(
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dep),
):
    """Return all users marked as reviewers (is_reviewer=True) for the assignment picker."""
    auth_dependency.secure_access("MANAGE_REVIEWERS", current_user["user_id"])
    users = (
        db.query(User)
        .filter(User.is_reviewer == True, User.deleted_at == None)
        .order_by(User.firstname, User.lastname)
        .all()
    )
    return [
        {"id": u.id, "firstname": u.firstname, "lastname": u.lastname, "email": u.email}
        for u in users
    ]


@router.get("/reviewers")
def list_reviewers(
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dep),
    event_id: int = None,
):
    auth_dependency.secure_access("MANAGE_REVIEWERS", current_user["user_id"])
    q = db.query(AbstractReviewer).options(
        joinedload(AbstractReviewer.reviewer),
        joinedload(AbstractReviewer.abstract).joinedload(Abstract.event),
        joinedload(AbstractReviewer.review),
    )
    if event_id:
        from sqlalchemy import join
        q = q.join(Abstract, AbstractReviewer.abstract_id == Abstract.id).filter(Abstract.event_id == event_id)
    assignments = q.all()

    reviewers: dict = {}
    for a in assignments:
        rid = a.reviewer_id
        if rid not in reviewers:
            reviewers[rid] = {
                "reviewer_id": rid,
                "name": f"{a.reviewer.firstname} {a.reviewer.lastname}" if a.reviewer else "",
                "email": a.reviewer.email if a.reviewer else "",
                "total": 0,
                "completed": 0,
                "assignments": [],
            }
        reviewers[rid]["total"] += 1
        if a.completed:
            reviewers[rid]["completed"] += 1
        reviewers[rid]["assignments"].append({
            "assignment_id": a.id,
            "abstract_id": a.abstract_id,
            "abstract_title": a.abstract.title if a.abstract else "",
            "event": a.abstract.event.event if a.abstract and a.abstract.event else "",
            "event_id": a.abstract.event_id if a.abstract else None,
            "assigned_at": a.assigned_at,
            "completed": a.completed,
        })
    return list(reviewers.values())


@router.get("/{abstract_id}")
def get_abstract(
    abstract_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
):
    abstract = db.query(Abstract).options(
        joinedload(Abstract.authors),
        joinedload(Abstract.submitter),
        joinedload(Abstract.event),
        joinedload(Abstract.event_track),
        joinedload(Abstract.reviewer_assignments).joinedload(AbstractReviewer.reviewer),
        joinedload(Abstract.reviewer_assignments).joinedload(AbstractReviewer.review),
    ).filter(Abstract.id == abstract_id, Abstract.deleted_at == None).first()
    if not abstract:
        raise HTTPException(status_code=404, detail="Abstract not found")
    return _serialize_abstract(abstract)


@router.put("/{abstract_id}")
def update_abstract(
    abstract_id: int,
    schema: AbstractUpdateSchema,
    current_user: user_dependency,
    db: Session = Depends(get_db),
):
    abstract = db.query(Abstract).filter(Abstract.id == abstract_id, Abstract.deleted_at == None).first()
    if not abstract:
        raise HTTPException(status_code=404, detail="Abstract not found")

    if schema.title: abstract.title = schema.title
    if schema.abstract_text:
        abstract.abstract_text = schema.abstract_text
        abstract.word_count = len(schema.abstract_text.split())
    if schema.keywords is not None: abstract.keywords = schema.keywords
    if schema.track is not None: abstract.track = schema.track
    if schema.presentation_type: abstract.presentation_type = schema.presentation_type
    if schema.status: abstract.status = schema.status

    if schema.authors is not None:
        db.query(AbstractAuthor).filter(AbstractAuthor.abstract_id == abstract_id).delete()
        for i, author in enumerate(schema.authors):
            db.add(AbstractAuthor(
                abstract_id=abstract_id,
                firstname=author.firstname,
                lastname=author.lastname,
                email=author.email,
                affiliation=author.affiliation,
                country=author.country,
                is_presenting=author.is_presenting,
                author_order=i,
            ))

    db.commit()
    db.refresh(abstract)
    abstract = db.query(Abstract).options(
        joinedload(Abstract.authors),
        joinedload(Abstract.submitter),
        joinedload(Abstract.event),
        joinedload(Abstract.reviewer_assignments).joinedload(AbstractReviewer.reviewer),
        joinedload(Abstract.reviewer_assignments).joinedload(AbstractReviewer.review),
    ).filter(Abstract.id == abstract_id).first()
    return _serialize_abstract(abstract)


@router.put("/{abstract_id}/status")
def update_status(
    abstract_id: int,
    payload: dict,
    current_user: user_dependency,
    db: Session = Depends(get_db),
):
    abstract = db.query(Abstract).filter(Abstract.id == abstract_id, Abstract.deleted_at == None).first()
    if not abstract:
        raise HTTPException(status_code=404, detail="Abstract not found")
    abstract.status = payload.get("status", abstract.status)
    db.commit()
    return {"message": "Status updated"}


@router.post("/bulk-assign-reviewer", status_code=status.HTTP_201_CREATED)
def bulk_assign_reviewer(
    schema: BulkAssignReviewerSchema,
    background_tasks: BackgroundTasks,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dep),
):
    """Assign one reviewer to multiple abstracts and send a single consolidated email."""
    auth_dependency.secure_access("MANAGE_REVIEWERS", current_user["user_id"])

    reviewer = db.query(User).filter(User.id == schema.reviewer_id).first()
    if not reviewer:
        raise HTTPException(status_code=404, detail="Reviewer not found")

    assigner = db.query(User).filter(User.id == current_user["user_id"]).first()
    assigner_name  = f"{assigner.firstname} {assigner.lastname}" if assigner else "ECSA Secretariat"
    assigner_email = assigner.email if assigner else None

    assigned_abstracts = []
    skipped = []

    for abstract_id in schema.abstract_ids:
        abstract = db.query(Abstract).options(joinedload(Abstract.event)).filter(
            Abstract.id == abstract_id, Abstract.deleted_at == None
        ).first()
        if not abstract:
            skipped.append({"id": abstract_id, "reason": "not found"})
            continue
        existing = db.query(AbstractReviewer).filter(
            AbstractReviewer.abstract_id == abstract_id,
            AbstractReviewer.reviewer_id == schema.reviewer_id,
        ).first()
        if existing:
            skipped.append({"id": abstract_id, "reason": "already assigned"})
            continue
        db.add(AbstractReviewer(
            abstract_id=abstract_id,
            reviewer_id=schema.reviewer_id,
            assigned_by=current_user["user_id"],
        ))
        assigned_abstracts.append(abstract)

    if not assigned_abstracts:
        db.commit()
        return {"message": "No new assignments made", "assigned": 0, "skipped": skipped}

    import utils.mailer_util as mailer_util

    new_password = None
    if not reviewer.credentials_sent:
        new_password = auth_dependency.generate_random_password()
        reviewer.hashed_password = auth_dependency.hash_password(new_password)
        reviewer.credentials_sent = True

    db.commit()

    mailer_util.reviewer_bulk_assignment_email(
        recipient_email=reviewer.email,
        firstname=reviewer.firstname,
        password=new_password,
        abstracts=[
            {"title": a.title, "event": a.event.event if a.event else ""}
            for a in assigned_abstracts
        ],
        assigned_by_name=assigner_name,
        assigned_by_email=assigner_email,
        sent_by_user_id=current_user["user_id"],
        background_tasks=background_tasks,
        db=db,
    )

    return {
        "message": f"{len(assigned_abstracts)} abstract(s) assigned to {reviewer.firstname} {reviewer.lastname}",
        "assigned": len(assigned_abstracts),
        "skipped": skipped,
    }


@router.post("/{abstract_id}/assign-reviewer", status_code=status.HTTP_201_CREATED)
def assign_reviewer(
    abstract_id: int,
    schema: AssignReviewerSchema,
    background_tasks: BackgroundTasks,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dep),
):
    auth_dependency.secure_access("MANAGE_REVIEWERS", current_user["user_id"])
    abstract = db.query(Abstract).options(
        joinedload(Abstract.event)
    ).filter(Abstract.id == abstract_id, Abstract.deleted_at == None).first()
    if not abstract:
        raise HTTPException(status_code=404, detail="Abstract not found")

    existing = db.query(AbstractReviewer).filter(
        AbstractReviewer.abstract_id == abstract_id,
        AbstractReviewer.reviewer_id == schema.reviewer_id,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Reviewer already assigned")

    reviewer = db.query(User).filter(User.id == schema.reviewer_id).first()
    if not reviewer:
        raise HTTPException(status_code=404, detail="Reviewer not found")

    assigner = db.query(User).filter(User.id == current_user["user_id"]).first()
    assigner_name  = f"{assigner.firstname} {assigner.lastname}" if assigner else "ECSA Secretariat"
    assigner_email = assigner.email if assigner else None

    assignment = AbstractReviewer(
        abstract_id=abstract_id,
        reviewer_id=schema.reviewer_id,
        assigned_by=current_user["user_id"],
    )
    db.add(assignment)

    import utils.mailer_util as mailer_util

    if not reviewer.credentials_sent:
        # First time this user is contacted — generate a fresh password and
        # include it in the assignment email so they can log in.
        new_password = auth_dependency.generate_random_password()
        reviewer.hashed_password = auth_dependency.hash_password(new_password)
        reviewer.credentials_sent = True
        db.commit()
        mailer_util.reviewer_assignment_email(
            recipient_email=reviewer.email,
            firstname=reviewer.firstname,
            password=new_password,
            abstract_title=abstract.title,
            event_name=abstract.event.event if abstract.event else None,
            assigned_by_name=assigner_name,
            assigned_by_email=assigner_email,
            sent_by_user_id=current_user["user_id"],
            background_tasks=background_tasks,
            db=db,
        )
    else:
        # Reviewer already has their credentials — just notify them of the new
        # assignment without touching their password.
        db.commit()
        mailer_util.reviewer_assignment_email(
            recipient_email=reviewer.email,
            firstname=reviewer.firstname,
            password=None,
            abstract_title=abstract.title,
            event_name=abstract.event.event if abstract.event else None,
            assigned_by_name=assigner_name,
            assigned_by_email=assigner_email,
            sent_by_user_id=current_user["user_id"],
            background_tasks=background_tasks,
            db=db,
        )

    return {"message": "Reviewer assigned", "reviewer_name": f"{reviewer.firstname} {reviewer.lastname}"}


@router.delete("/{abstract_id}/reviewers/{reviewer_id}")
def remove_reviewer(
    abstract_id: int,
    reviewer_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dep),
):
    auth_dependency.secure_access("MANAGE_REVIEWERS", current_user["user_id"])
    assignment = db.query(AbstractReviewer).filter(
        AbstractReviewer.abstract_id == abstract_id,
        AbstractReviewer.reviewer_id == reviewer_id,
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(assignment)
    db.commit()
    return {"message": "Reviewer removed"}


@router.delete("/{abstract_id}")
def delete_abstract(
    abstract_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dep),
):
    auth_dependency.secure_access("MANAGE_REVIEWERS", current_user["user_id"])
    abstract = db.query(Abstract).filter(Abstract.id == abstract_id, Abstract.deleted_at == None).first()
    if not abstract:
        raise HTTPException(status_code=404, detail="Abstract not found")
    abstract.deleted_at = datetime.utcnow()
    db.commit()
    return {"message": "Abstract deleted"}


@router.post("/reviewers/create", status_code=status.HTTP_201_CREATED)
def create_reviewer(
    schema: CreateReviewerSchema,
    current_user: user_dependency,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dep),
):
    """Create a new user account designated as a reviewer and send them login credentials."""
    auth_dependency.secure_access("MANAGE_REVIEWERS", current_user["user_id"])

    existing = db.query(User).filter(User.email == schema.email).first()
    if existing:
        # User already exists — mark them as a reviewer and return their data
        existing.is_reviewer = True
        db.commit()
        return {
            "id": existing.id,
            "firstname": existing.firstname,
            "lastname": existing.lastname,
            "email": existing.email,
        }

    # Get or create the phone (phone optional for reviewers — use email as fallback stub)
    phone = schema.phone or schema.email

    password = auth_dependency.generate_random_password()
    hashed = auth_dependency.hash_password(password)

    user = User(
        firstname=schema.firstname,
        lastname=schema.lastname,
        email=schema.email,
        phone=phone,
        hashed_password=hashed,
        verified=True,
        is_reviewer=True,
    )
    db.add(user)
    db.flush()

    # Assign "User" role so they can log in
    user_role = db.query(Role).filter(Role.role == "User").first()
    if user_role:
        db.add(UserRole(user_id=user.id, role_id=user_role.id))

    db.commit()
    db.refresh(user)

    # Credentials are intentionally NOT sent here — they will be emailed
    # automatically when the reviewer is first assigned to an abstract.

    return {
        "id": user.id,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
    }


@router.post("/reviews/{assignment_id}", status_code=status.HTTP_201_CREATED)
def submit_review(
    assignment_id: int,
    schema: AbstractReviewSchema,
    current_user: user_dependency,
    db: Session = Depends(get_db),
):
    assignment = db.query(AbstractReviewer).filter(
        AbstractReviewer.id == assignment_id,
        AbstractReviewer.reviewer_id == current_user["user_id"],
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    if assignment.review:
        raise HTTPException(status_code=400, detail="Review already submitted")

    review = AbstractReview(
        assignment_id=assignment_id,
        relevance_score=schema.relevance_score,
        methodology_score=schema.methodology_score,
        originality_score=schema.originality_score,
        overall_score=schema.overall_score,
        recommendation=schema.recommendation,
        comments=schema.comments,
        confidential_comments=schema.confidential_comments,
    )
    db.add(review)
    assignment.completed = True
    db.commit()
    return {"message": "Review submitted successfully"}


@router.get("/{abstract_id}/reviews")
def get_reviews(
    abstract_id: int,
    current_user: user_dependency,
    db: Session = Depends(get_db),
):
    assignments = db.query(AbstractReviewer).options(
        joinedload(AbstractReviewer.reviewer),
        joinedload(AbstractReviewer.review),
    ).filter(AbstractReviewer.abstract_id == abstract_id).all()
    return [
        {
            "assignment_id": a.id,
            "reviewer": f"{a.reviewer.firstname} {a.reviewer.lastname}" if a.reviewer else None,
            "completed": a.completed,
            "review": {
                "relevance_score": a.review.relevance_score,
                "methodology_score": a.review.methodology_score,
                "originality_score": a.review.originality_score,
                "overall_score": a.review.overall_score,
                "recommendation": a.review.recommendation.value,
                "comments": a.review.comments,
                "submitted_at": a.review.submitted_at,
            } if a.review else None,
        }
        for a in assignments
    ]


# ══════════════════════════════════════════════════════════════════════════════
#  TRACKS  endpoints
# ══════════════════════════════════════════════════════════════════════════════

from pydantic import BaseModel as PydanticBase
from typing import Optional

class TrackUpdateSchema(PydanticBase):
    code:       Optional[str] = None
    title:      Optional[str] = None
    theme:      Optional[str] = None
    sort_order: Optional[int] = None


def _serialize_track(t: EventTrack, abstract_count: int = 0) -> dict:
    return {
        "id":             t.id,
        "event_id":       t.event_id,
        "event":          t.event.event if t.event else None,
        "code":           t.code,
        "title":          t.title,
        "theme":          t.theme,
        "sort_order":     t.sort_order,
        "abstract_count": abstract_count,
        "created_at":     t.created_at,
    }


@router.get("/tracks/list")
def list_tracks(
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dep),
    event_id: int = None,
):
    auth_dependency.secure_access("VIEW_ABSTRACTS", current_user["user_id"])
    from sqlalchemy import func as sqlfunc
    q = db.query(
        EventTrack,
        sqlfunc.count(Abstract.id).label("abstract_count")
    ).outerjoin(
        Abstract,
        (Abstract.track_id == EventTrack.id) & (Abstract.deleted_at == None)
    ).options(joinedload(EventTrack.event))
    if event_id:
        q = q.filter(EventTrack.event_id == event_id)
    rows = q.group_by(EventTrack.id).order_by(EventTrack.sort_order, EventTrack.code).all()
    return [_serialize_track(t, cnt) for t, cnt in rows]


@router.get("/tracks/public")
def list_tracks_public(
    db: Session = Depends(get_db),
    event_id: int = None,
):
    """Public endpoint — no auth required. Returns tracks for the submission form."""
    q = db.query(EventTrack)
    if event_id:
        q = q.filter(EventTrack.event_id == event_id)
    rows = q.order_by(EventTrack.sort_order, EventTrack.code).all()
    return [
        {"id": t.id, "code": t.code, "title": t.title, "theme": t.theme, "sort_order": t.sort_order}
        for t in rows
    ]


@router.put("/tracks/{track_id}")
def update_track(
    track_id: int,
    schema: TrackUpdateSchema,
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dep),
):
    auth_dependency.secure_access("VIEW_ABSTRACTS", current_user["user_id"])
    track = db.query(EventTrack).options(joinedload(EventTrack.event)).filter(EventTrack.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    if schema.code       is not None: track.code       = schema.code
    if schema.title      is not None: track.title      = schema.title
    if schema.theme      is not None: track.theme      = schema.theme
    if schema.sort_order is not None: track.sort_order = schema.sort_order
    if schema.code is not None or schema.title is not None:
        new_text = f"{track.code}: {track.title}"
        db.query(Abstract).filter(Abstract.track_id == track_id).update(
            {"track": new_text}, synchronize_session=False
        )
    db.commit()
    db.refresh(track)
    from sqlalchemy import func as sqlfunc
    cnt = db.query(sqlfunc.count(Abstract.id)).filter(
        Abstract.track_id == track_id, Abstract.deleted_at == None
    ).scalar() or 0
    return _serialize_track(track, cnt)
