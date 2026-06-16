from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session, joinedload

from core.database import SessionLocal
from models.models import AbstractReviewer, Abstract
import utils.mailer_util as mailer_util
import logging

logger = logging.getLogger(__name__)

REMINDER_THRESHOLD_HOURS = 48


def send_pending_review_reminders():
    db: Session = SessionLocal()
    try:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=REMINDER_THRESHOLD_HOURS)

        overdue = (
            db.query(AbstractReviewer)
            .options(
                joinedload(AbstractReviewer.reviewer),
                joinedload(AbstractReviewer.abstract).joinedload(Abstract.event),
            )
            .filter(
                AbstractReviewer.assigned_at <= cutoff,
                AbstractReviewer.completed == False,
                AbstractReviewer.reminder_sent_at == None,
            )
            .all()
        )

        for assignment in overdue:
            reviewer = assignment.reviewer
            abstract = assignment.abstract
            if not reviewer or not abstract:
                continue

            event_name = abstract.event.event if abstract.event else None

            try:
                # Claim the row first to avoid duplicate sends across workers
                assignment.reminder_sent_at = datetime.now(timezone.utc)
                db.commit()

                mailer_util.reviewer_reminder_email(
                    recipient_email=reviewer.email,
                    firstname=reviewer.firstname,
                    abstract_title=abstract.title,
                    assigned_at=assignment.assigned_at,
                    event_name=event_name,
                    db=db,
                )
                logger.info("Reminder sent to %s for abstract %s", reviewer.email, abstract.id)
            except Exception as e:
                logger.error("Failed to send reminder to %s: %s", reviewer.email, e)

    except Exception as e:
        logger.error("Error in send_pending_review_reminders: %s", e)
    finally:
        db.close()


def start_scheduler():
    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.add_job(
        send_pending_review_reminders,
        trigger="interval",
        hours=1,
        next_run_time=datetime.now(timezone.utc),
        id="reviewer_reminder",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler started — reviewer reminder job runs every hour.")
    return scheduler
