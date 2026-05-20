"""
One-time script to insert the new permissions added in recent updates.
Safe to re-run — skips any permission that already exists.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from core.database import SessionLocal
from models.models import Permission

NEW_PERMISSIONS = [
    ("View Abstracts",       "VIEW_ABSTRACTS",       "EVENTS_SPACE"),
    ("Export Abstracts",     "EXPORT_ABSTRACTS",     "EVENTS_SPACE"),
    ("Manage Reviewers",     "MANAGE_REVIEWERS",     "EVENTS_SPACE"),
    ("View Registrations",   "VIEW_REGISTRATIONS",   "EVENTS_SPACE"),
    ("Export Registrations", "EXPORT_REGISTRATIONS", "EVENTS_SPACE"),
    ("View Statistics",      "VIEW_STATS",           "EVENTS_SPACE"),
]

db = SessionLocal()
try:
    added = 0
    for name, code, system in NEW_PERMISSIONS:
        exists = db.query(Permission).filter(Permission.permission_code == code).first()
        if exists:
            print(f"  SKIP  {code} (already exists)")
        else:
            db.add(Permission(permission=name, permission_code=code, system_code=system))
            print(f"  ADD   {code}")
            added += 1
    db.commit()
    print(f"\nDone — {added} permission(s) inserted.")
finally:
    db.close()
