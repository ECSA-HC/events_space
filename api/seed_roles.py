"""
Creates the three new restricted roles and assigns their permissions.
Safe to re-run — skips anything that already exists.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from core.database import SessionLocal
from models.models import Role, Permission, RolePermission

ROLES = [
    {
        "role": "Statistics Viewer",
        "description": "Can view the admin dashboard and browse the abstracts and registrations lists.",
        "permissions": ["VIEW_STATS", "VIEW_ABSTRACTS", "VIEW_REGISTRATIONS"],
    },
    {
        "role": "Abstract Viewer",
        "description": "Can view and export the abstracts list and event registrations list.",
        "permissions": [
            "VIEW_STATS",
            "VIEW_ABSTRACTS",
            "EXPORT_ABSTRACTS",
            "VIEW_REGISTRATIONS",
            "EXPORT_REGISTRATIONS",
        ],
    },
    {
        "role": "Reviewer Manager",
        "description": "Can view abstracts and manage reviewer assignments.",
        "permissions": [
            "VIEW_STATS",
            "VIEW_ABSTRACTS",
            "EXPORT_ABSTRACTS",
            "MANAGE_REVIEWERS",
        ],
    },
]

db = SessionLocal()
try:
    # Build permission lookup
    all_perms = {p.permission_code: p for p in db.query(Permission).all()}

    for role_def in ROLES:
        role = db.query(Role).filter(Role.role == role_def["role"]).first()
        if not role:
            role = Role(role=role_def["role"], description=role_def["description"])
            db.add(role)
            db.flush()
            print(f"  CREATED role: {role_def['role']}")
        else:
            print(f"  EXISTS  role: {role_def['role']}")

        for code in role_def["permissions"]:
            perm = all_perms.get(code)
            if not perm:
                print(f"    MISSING permission {code} — run seed_permissions.py first")
                continue
            exists = db.query(RolePermission).filter(
                RolePermission.role_id == role.id,
                RolePermission.permission_id == perm.id,
            ).first()
            if not exists:
                db.add(RolePermission(role_id=role.id, permission_id=perm.id))
                print(f"    + {code}")
            else:
                print(f"    ~ {code} (already assigned)")

    db.commit()
    print("\nDone.")
finally:
    db.close()
