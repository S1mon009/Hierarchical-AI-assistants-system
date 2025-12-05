from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class AppMetadata(BaseModel):
    provider: str
    providers: List[str]


class UserMetadata(BaseModel):
    display_name: str
    email: EmailStr
    email_verified: bool
    phone_verified: bool
    sub: str


class IdentityData(BaseModel):
    display_name: str
    email: EmailStr
    email_verified: bool
    phone_verified: bool
    sub: str


class Identity(BaseModel):
    id: str
    identity_id: str
    user_id: str
    identity_data: IdentityData
    provider: str
    created_at: datetime
    last_sign_in_at: datetime
    updated_at: datetime


class RetrieveUserResponseModel(BaseModel):
    id: str
    app_metadata: AppMetadata
    user_metadata: UserMetadata
    aud: str
    confirmation_sent_at: Optional[datetime]
    recovery_sent_at: Optional[datetime]
    email_change_sent_at: Optional[datetime]
    new_email: Optional[str]
    new_phone: Optional[str]
    invited_at: Optional[datetime]
    action_link: Optional[str]
    email: EmailStr
    phone: Optional[str]
    created_at: datetime
    confirmed_at: Optional[datetime]
    email_confirmed_at: Optional[datetime]
    phone_confirmed_at: Optional[datetime]
    last_sign_in_at: Optional[datetime]
    role: str
    updated_at: datetime
    identities: List[Identity]
    is_anonymous: bool
    factors: Optional[List] = None
