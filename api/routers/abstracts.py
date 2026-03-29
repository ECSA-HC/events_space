from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from core.database import get_db
from dependencies.auth_dependency import get_current_user
from models.models import Abstract, AbstractAuthor, AbstractReviewer, AbstractReview, User
from schemas.events_space import (
    AbstractSubmitSchema, AbstractUpdateSchema,
    AssignReviewerSchema, AbstractReviewSchema
)

router = APIRouter()

user_dependency = get_current_user


def _serialize_abstract(a: Abstract):
    return {
        "id": a.id,
        "event_id": a.event_id,
        "event": a.event.event if a.event else None,
        "title": a.title,
        "abstract_text": a.abstract_text,
        "keywords": a.keywords,
        "track": a.track,
        "presentation_type": a.presentation_type.value if a.presentation_type else None,
        "status": a.status.value if a.status else None,
        "word_count": a.word_count,
        "submitted_by": a.submitted_by,
        "submitter_name": f"{a.submitter.firstname} {a.submitter.lastname}" if a.submitter else None,
        "submitter_email": a.submitter.email if a.submitter else None,
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
    schema: AbstractSubmitSchema,
    current_user: dict = Depends(user_dependency),
    db: Session = Depends(get_db),
):
    word_count = len(schema.abstract_text.split())
    abstract = Abstract(
        event_id=schema.event_id,
        submitted_by=current_user["user_id"],
        title=schema.title,
        abstract_text=schema.abstract_text,
        keywords=schema.keywords,
        track=schema.track,
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
    # reload with relationships
    abstract = db.query(Abstract).options(
        joinedload(Abstract.authors),
        joinedload(Abstract.submitter),
        joinedload(Abstract.event),
        joinedload(Abstract.reviewer_assignments),
    ).filter(Abstract.id == abstract.id).first()
    return _serialize_abstract(abstract)


@router.get("/")
def list_abstracts(
    event_id: int = None,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(user_dependency),
    db: Session = Depends(get_db),
):
    q = db.query(Abstract).options(
        joinedload(Abstract.authors),
        joinedload(Abstract.submitter),
        joinedload(Abstract.event),
        joinedload(Abstract.reviewer_assignments).joinedload(AbstractReviewer.reviewer),
        joinedload(Abstract.reviewer_assignments).joinedload(AbstractReviewer.review),
    ).filter(Abstract.deleted_at == None)
    if event_id:
        q = q.filter(Abstract.event_id == event_id)
    abstracts = q.order_by(Abstract.created_at.desc()).offset(skip).limit(limit).all()
    return [_serialize_abstract(a) for a in abstracts]


@router.get("/my-submissions")
def my_submissions(
    current_user: dict = Depends(user_dependency),
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
    current_user: dict = Depends(user_dependency),
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


@router.get("/{abstract_id}")
def get_abstract(
    abstract_id: int,
    current_user: dict = Depends(user_dependency),
    db: Session = Depends(get_db),
):
    abstract = db.query(Abstract).options(
        joinedload(Abstract.authors),
        joinedload(Abstract.submitter),
        joinedload(Abstract.event),
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
    current_user: dict = Depends(user_dependency),
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
    current_user: dict = Depends(user_dependency),
    db: Session = Depends(get_db),
):
    abstract = db.query(Abstract).filter(Abstract.id == abstract_id, Abstract.deleted_at == None).first()
    if not abstract:
        raise HTTPException(status_code=404, detail="Abstract not found")
    abstract.status = payload.get("status", abstract.status)
    db.commit()
    return {"message": "Status updated"}


@router.post("/{abstract_id}/assign-reviewer", status_code=status.HTTP_201_CREATED)
def assign_reviewer(
    abstract_id: int,
    schema: AssignReviewerSchema,
    current_user: dict = Depends(user_dependency),
    db: Session = Depends(get_db),
):
    abstract = db.query(Abstract).filter(Abstract.id == abstract_id, Abstract.deleted_at == None).first()
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

    assignment = AbstractReviewer(
        abstract_id=abstract_id,
        reviewer_id=schema.reviewer_id,
        assigned_by=current_user["user_id"],
    )
    db.add(assignment)
    db.commit()
    return {"message": "Reviewer assigned", "reviewer_name": f"{reviewer.firstname} {reviewer.lastname}"}


@router.delete("/{abstract_id}/reviewers/{reviewer_id}")
def remove_reviewer(
    abstract_id: int,
    reviewer_id: int,
    current_user: dict = Depends(user_dependency),
    db: Session = Depends(get_db),
):
    assignment = db.query(AbstractReviewer).filter(
        AbstractReviewer.abstract_id == abstract_id,
        AbstractReviewer.reviewer_id == reviewer_id,
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(assignment)
    db.commit()
    return {"message": "Reviewer removed"}


@router.post("/reviews/{assignment_id}", status_code=status.HTTP_201_CREATED)
def submit_review(
    assignment_id: int,
    schema: AbstractReviewSchema,
    current_user: dict = Depends(user_dependency),
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
    current_user: dict = Depends(user_dependency),
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
