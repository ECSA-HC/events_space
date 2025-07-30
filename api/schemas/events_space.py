from pydantic import BaseModel, EmailStr, field_validator, model_validator, HttpUrl
from datetime import date, datetime

import re


class UserSchema(BaseModel):
    firstname: str
    lastname: str
    phone: str
    email: EmailStr

    @field_validator("phone")
    def validate_phone(cls, value):
        phone_regex = r"^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$"
        if not re.match(phone_regex, value):
            raise ValueError("Invalid phone number format")
        return value


class ProfileSchema(BaseModel):
    title: str
    middle_name: str
    country_id: int
    gender: str
    organisation: str
    position: str
    profession: str


class EmailSchema(BaseModel):
    email: EmailStr


class AuthSchema(BaseModel):
    username: EmailStr
    password: str


class PasswordResetSchema(BaseModel):
    password: str
    rest_token: str


class VerificationTokenSchema(BaseModel):
    verification_token: str


class RoleSchema(BaseModel):
    role: str
    description: str


class UserRoleSchema(BaseModel):
    user_id: int
    role_id: int


class PermissionSchema(BaseModel):
    permission: str
    system_code: str
    permission_code: str


class RolePermissionSchema(BaseModel):
    role_id: int
    permission_id: int


class CountrySchema(BaseModel):
    country: str
    short_code: str
    phone_code: str


class OrgUnitSchema(BaseModel):
    name: str
    type: str
    description: str


class EventSchema(BaseModel):
    org_unit_id: int
    country_id: int
    event: str
    theme: str
    description: str
    start_date: date
    end_date: date
    location: str

    @field_validator("start_date", "end_date")
    def check_dates_not_in_past(cls, v: date):
        if v < date.today():
            raise ValueError("Date must be today or in the future")
        return v

    @model_validator(mode="after")
    def check_date_order(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date must be after or equal to start_date")
        return self


class RegistrationSchema(BaseModel):
    event_id: int
    participation_role: str


class OrganisationSchema(BaseModel):
    country_id: int
    organisation: str
    organisation_type: str
    sector: str
    address: str
    city: str
    email: EmailStr
    phone_number: str
    is_donor: int
    is_recipient: int


class OrganisationIDSchema(BaseModel):
    organisation_id: int


class OrganisationApprovalSchema(BaseModel):
    organisation_id: int
    is_approved: str
    comment: str


class LinkSchema(BaseModel):
    event_id: int
    name: str
    link: HttpUrl


class AttendanceBase(BaseModel):
    registration_id: int


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceRead(AttendanceBase):
    id: int
    attendance_date: datetime

    class Config:
        orm_mode = True
