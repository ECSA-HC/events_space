from enum import Enum as PyEnum
from sqlalchemy.sql import func
from sqlalchemy import Numeric
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Boolean,
    TIMESTAMP,
    UniqueConstraint,
    JSON,
    Enum,
    Index,
)
from datetime import datetime
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class OrganisationType(PyEnum):
    Non_profit = "Non_profit"
    Corporation = "Corporation"
    Government = "Government"
    Other = "Other"


class SectorType(PyEnum):
    Technology = "Technology"
    Education = "Education"
    Healthcare = "Healthcare"
    Finance = "Finance"
    Other = "Other"


class DocumentType(PyEnum):
    ProgrammeBooklet = "ProgrammeBooklet"
    Presentation = "Presentation"
    Photo = "Photo"
    Advert = "Advert"
    Guidelines = "Guidelines"
    Other = "Other"


class OrganisationStatus(PyEnum):
    Pending = "Pending"
    Approved = "Approved"
    Denied = "Denied"


class OrgUnitType(PyEnum):
    project = "project"
    department = "department"
    college = "college"
    secretariat = "secretariat"
    other = "other"


class ParticipationRole(PyEnum):
    secretariat = "secretariat"
    delegate = "delegate"
    presenter = "presenter"
    speaker = "speaker"
    sponsor = "sponsor"
    moderator = "moderator"
    participant = "participant"
    student = "student"
    exhibitor = "exhibitor"
    world = "world"
    other_africa = "other_africa"
    member_state = "member_state"
    moh = "moh"


class PaymentMethod(PyEnum):
    CASH = "Cash"
    MPESA = "Mpesa"
    BANK_TRANSFER = "Bank Transfer"
    CARD = "Card"


class PaymentStatus(PyEnum):
    PENDING = "Pending"
    COMPLETED = "Completed"


class BaseWithSoftDelete(Base):
    __abstract__ = True

    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    @classmethod
    def filter_deleted(cls, query):
        return query.filter(cls.deleted_at is None)


class User(BaseWithSoftDelete):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(45), nullable=False)
    lastname = Column(String(45), nullable=False)
    phone = Column(String(25), nullable=False, unique=True)
    email = Column(String(45), nullable=False, unique=True)
    hashed_password = Column(String(200), nullable=False)
    verified = Column(Boolean, nullable=False, server_default="False")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    user_roles = relationship("UserRole", back_populates="user")
    events = relationship("Event", back_populates="user")
    registrations = relationship("Registration", back_populates="user")
    user_photo = relationship("UserPhoto", back_populates="user")
    user_profile = relationship("UserProfile", back_populates="user")

    __table_args__ = (Index("ix_user", "deleted_at", "email", "phone", "id"),)

    def __repr__(self):
        return f"<User {self.id}>"


class UserProfile(BaseWithSoftDelete):
    __tablename__ = "user_profile"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    country_id = Column(Integer, ForeignKey("country.id"), nullable=False)
    title = Column(String(10), nullable=False)
    middle_name = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    position = Column(String(200), nullable=True)
    organisation = Column(String(200), nullable=True)
    profession = Column(String(200), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    user = relationship("User", back_populates="user_profile")
    country = relationship("Country", back_populates="user_profile")

    __table_args__ = (Index("ix_user_profile", "user_id", "deleted_at"),)

    def __repr__(self):
        return f"<UserProfile user_id={self.user_id}, gender={self.gender}>"


class UserPhoto(BaseWithSoftDelete):
    __tablename__ = "user_photo"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    path = Column(Text, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    user = relationship("User", back_populates="user_photo")

    __table_args__ = (Index("ix_user_photo", "user_id", "deleted_at"),)

    def __repr__(self):
        return f"<UserPhoto user_id={self.user_id}, path={self.path}>"


class Role(BaseWithSoftDelete):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(
        String(45),
        unique=True,
    )
    description = Column(
        Text,
        nullable=False,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    user_roles = relationship("UserRole", back_populates="role")

    role_permissions = relationship("RolePermission", back_populates="role")

    __table_args__ = (Index("ix_role", "role", "deleted_at"),)

    def __repr__(self):
        return f"<Role {self.id}"


class UserRole(BaseWithSoftDelete):
    __tablename__ = "user_role"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")

    __table_args__ = (
        UniqueConstraint(user_id, role_id, name="user_id_role_id"),
        Index("ix_user_role", "user_id", "role_id", "deleted_at"),
    )

    def __repr__(self):
        return f"<UserRole user_id={self.user_id}, role_id={self.role_id}>"


class Permission(BaseWithSoftDelete):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, index=True)
    permission = Column(
        String(45),
        unique=True,
        nullable=False,
    )
    permission_code = Column(String(45), unique=True, nullable=False)
    system_code = Column(String(45), unique=False, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    role_permissions = relationship("RolePermission", back_populates="permission")

    __table_args__ = (Index("ix_permission", "permission", "deleted_at"),)

    def __repr__(self):
        return f"<Permission {self.permission}"


class RolePermission(BaseWithSoftDelete):
    __tablename__ = "role_permission"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("role.id", ondelete="CASCADE"), nullable=False)
    permission_id = Column(
        Integer, ForeignKey("permission.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    role = relationship("Role", back_populates="role_permissions")
    permission = relationship("Permission", back_populates="role_permissions")

    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="role_id_permission_id"),
        Index("ix_role_permission", "role_id", "permission_id", "deleted_at"),
    )

    def __repr__(self):
        return f"<RolePermission role_id={self.role_id}, permission_id={self.permission_id}>"


class Country(BaseWithSoftDelete):
    __tablename__ = "country"
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(100), unique=True, index=True)
    short_code = Column(String(5), unique=True, index=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    events = relationship("Event", back_populates="country")
    user_profile = relationship("UserProfile", back_populates="country")

    Index("ix_country_deleted_at", "country", "deleted_at")

    def __repr__(self):
        return f"<Country {self.id}>"


class ActivityLog(BaseWithSoftDelete):
    __tablename__ = "activity_log"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    action = Column(String, nullable=False)
    target = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    additional_data = Column(JSON, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    __table_args__ = (Index("ix_activity_log", "action", "deleted_at"),)

    def __repr__(self):
        return f"<ActivityLog {self.id}>"


class PasswordReset(BaseWithSoftDelete):
    __tablename__ = "password_reset"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    reset_token = Column(String, nullable=False, unique=True, index=True)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    __table_args__ = (Index("ix_password_reset", "deleted_at"),)

    def __repr__(self):
        return f"<PasswordReset {self.id}>"


class AccountVerification(BaseWithSoftDelete):
    __tablename__ = "account_verification"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    verification_token = Column(String, nullable=False, unique=True, index=True)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    __table_args__ = (Index("ix_account_verification", "deleted_at"),)

    def __repr__(self):
        return f"<AccountVerification {self.id}>"


class OrgUnit(Base):
    __tablename__ = "org_unit"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    type = Column(Enum(OrgUnitType), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    events = relationship("Event", back_populates="org_unit")

    def __repr__(self):
        return f"<OrgUnit id={self.id}, name={self.name}, type={self.type}>"


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("user.id"), nullable=False
    )  # link event to org unit (project/department/college)
    org_unit_id = Column(
        Integer, ForeignKey("org_unit.id"), nullable=False
    )  # link event to org unit (project/department/college)
    country_id = Column(
        Integer, ForeignKey("country.id"), nullable=False
    )  # link event to org unit (project/department/college)
    event = Column(Text, nullable=False)
    theme = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    location = Column(String(200), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    org_unit = relationship("OrgUnit", back_populates="events")
    country = relationship("Country", back_populates="events")
    user = relationship("User", back_populates="events")
    registrations = relationship("Registration", back_populates="events")
    documents = relationship("Document", back_populates="events")
    links = relationship("Link", back_populates="events")

    def __repr__(self):
        return f"<Event id={self.id}, name={self.name}>"


class Registration(Base):
    __tablename__ = "registration"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)
    participation_role = Column(Enum(ParticipationRole), nullable=False)
    paid = Column(Boolean, nullable=False, default=False)
    registered_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    user = relationship("User", back_populates="registrations")
    events = relationship("Event", back_populates="registrations")
    payment = relationship(
        "Payment",
        back_populates="registration",
        uselist=False,
        cascade="all, delete-orphan",
    )
    event_attendance = relationship("EventAttendance", back_populates="registration")

    __table_args__ = (
        UniqueConstraint("user_id", "event_id", name="unique_user_event_registration"),
    )

    def __repr__(self):
        return f"<Registration user_id={self.user_id} event_id={self.event_id} paid={self.paid}>"


class Payment(Base):
    __tablename__ = "payment"

    id = Column(Integer, primary_key=True, index=True)
    registration_id = Column(
        Integer, ForeignKey("registration.id", ondelete="CASCADE"), nullable=False
    )

    payment_date = Column(TIMESTAMP(timezone=True), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    payment_reference = Column(String(100), nullable=False)  # transaction ID/reference
    payment_amount = Column(Numeric(10, 2), nullable=False)
    payment_status = Column(Enum(PaymentStatus), nullable=False)
    payment_receipt = Column(
        String(255), nullable=True
    )  # file path or URL to the receipt

    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    registration = relationship("Registration", back_populates="payment")

    __table_args__ = (UniqueConstraint("registration_id", name="unique_payment"),)

    def __repr__(self):
        return f"<Payment registration_id={self.registration_id} paid={self.payment_amount}>"


class Document(BaseWithSoftDelete):
    __tablename__ = "document"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(
        Integer, ForeignKey("event.id", ondelete="CASCADE"), nullable=False
    )
    document_type = Column(Enum(DocumentType, validate_strings=True), nullable=False)
    file_type = Column(String(200), nullable=False)
    file_name = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    path = Column(Text, nullable=False)
    access_level = Column(Text, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    events = relationship("Event", back_populates="documents")

    __table_args__ = (Index("ix_document", "document_type", "deleted_at"),)

    def __repr__(self):
        return f"<Document document_type={self.document_type}, path={self.path}>"


class Link(BaseWithSoftDelete):
    __tablename__ = "link"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(
        Integer, ForeignKey("event.id", ondelete="CASCADE"), nullable=False
    )
    link = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    events = relationship("Event", back_populates="links")

    __table_args__ = (Index("ix_document", "link", "deleted_at"),)

    def __repr__(self):
        return f"<Link link={self.link}, name={self.name}>"


class EventAttendance(Base):
    __tablename__ = "event_attendance"

    id = Column(Integer, primary_key=True, index=True)
    registration_id = Column(Integer, ForeignKey("registration.id"), nullable=False)

    attendance_date = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    registration = relationship("Registration", back_populates="event_attendance")

    __table_args__ = (
        UniqueConstraint(
            "registration_id", "attendance_date", name="unique_event_attendance"
        ),
    )

    def __repr__(self):
        return f"<EventAttendance registration_id={self.registration_id}>"


# class Document(Base):
#     __tablename__ = "document"

#     id = Column(Integer, primary_key=True, index=True)
#     filename = Column(Text, nullable=False)
#     filepath = Column(Text, nullable=False)
#     file_name = Column(Text, nullable=False)
#     access_level = Column(Text, nullable=True)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
#     updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
#     deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

#     events = relationship("Event", back_populates="document")

#     def __repr__(self):
#         return f"<document id={self.id}, name={self.name}, type={self.type}>"


# This is un used database from here going down


class Organisation(BaseWithSoftDelete):
    __tablename__ = "organisation"

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(
        Integer, ForeignKey("country.id", ondelete="CASCADE"), nullable=False
    )
    created_by_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    organisation = Column(String(200), unique=False, nullable=False)
    organisation_type = Column(Enum(OrganisationType), nullable=False)
    sector = Column(Enum(SectorType), nullable=False)
    address = Column(Text, nullable=False)
    city = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    phone_number = Column(Text, nullable=False)
    is_verified = Column(Boolean, default=False)
    is_donor = Column(Boolean, default=False)
    is_recipient = Column(Boolean, default=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint("organisation", "country_id", name="uix_organisation_country"),
        Index("ix_organisation_country", "organisation", "country_id", "deleted_at"),
    )

    registrations = relationship(
        "OrganisationRegistration", back_populates="organisations"
    )
    documents = relationship("OrganisationDocument", back_populates="organisations")
    verification_requests = relationship(
        "OrganisationVerificationRequest", back_populates="organisations"
    )
    approval_statuses = relationship(
        "OrganisationApprovalStatus", back_populates="organisations"
    )

    def __repr__(self):
        return f"<Organisation id={self.id}, name={self.organisation}, country_id={self.country_id}>"


class OrganisationRegistration(BaseWithSoftDelete):
    __tablename__ = "organisation_registration"

    id = Column(Integer, primary_key=True, index=True)
    organisation_id = Column(
        Integer, ForeignKey("organisation.id", ondelete="CASCADE"), nullable=False
    )
    registration_number = Column(String(45), unique=True, nullable=False)
    registration_date = Column(TIMESTAMP(timezone=True), nullable=False)
    founders = Column(Text, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    organisations = relationship("Organisation", back_populates="registrations")

    __table_args__ = (
        Index("ix_organisation_registration", "registration_number", "deleted_at"),
    )

    def __repr__(self):
        return (
            f"<OrganisationRegistration registration_number={self.registration_number}>"
        )


class OrganisationDocument(BaseWithSoftDelete):
    __tablename__ = "organisation_document"

    id = Column(Integer, primary_key=True, index=True)
    organisation_id = Column(
        Integer, ForeignKey("organisation.id", ondelete="CASCADE"), nullable=False
    )
    document_type = Column(Enum(DocumentType), nullable=False)
    path = Column(Text, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    organisations = relationship("Organisation", back_populates="documents")

    __table_args__ = (Index("ix_organisation_document", "document_type", "deleted_at"),)

    def __repr__(self):
        return f"<OrganisationDocument document_type={self.document_type}, path={self.path}>"


class OrganisationVerificationRequest(BaseWithSoftDelete):
    __tablename__ = "organisation_verification_request"

    id = Column(Integer, primary_key=True, index=True)
    submitted_by_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    organisation_id = Column(
        Integer, ForeignKey("organisation.id", ondelete="CASCADE"), nullable=False
    )
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    organisations = relationship("Organisation", back_populates="verification_requests")

    __table_args__ = (
        Index("ix_organisation_verification_request", "organisation_id", "deleted_at"),
    )

    @validates("expires_at")
    def validate_expires_at(self, key, expires_at):
        # Validate if expires_at is in the future
        if expires_at < datetime.now():
            raise ValueError("Expires date cannot be in the past.")
        return expires_at

    def __repr__(self):
        return f"<OrganisationVerificationRequest id={self.id}, is_verified={self.is_verified}>"


class OrganisationApprovalStatus(BaseWithSoftDelete):
    __tablename__ = "organisation_approval_status"

    id = Column(Integer, primary_key=True, index=True)
    approved_by_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    organisation_id = Column(
        Integer, ForeignKey("organisation.id", ondelete="CASCADE"), nullable=False
    )
    is_approved = Column(Enum(OrganisationStatus), nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    organisations = relationship("Organisation", back_populates="approval_statuses")

    __table_args__ = (
        Index("ix_organisation_approval_status", "organisation_id", "deleted_at"),
    )

    def __repr__(self):
        return (
            f"<OrganisationApprovalStatus id={self.id}, is_approved={self.is_approved}>"
        )
