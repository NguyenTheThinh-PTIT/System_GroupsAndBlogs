from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str

class UserUpdate(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str

class UserOut(BaseModel):
    user_id: int
    username: str
    email: str
    full_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class GroupResponse(BaseModel):
    group_id: int
    group_name: str
    created_at: datetime
    class Config:
        from_attributes = True

class GroupCreate(BaseModel):
    group_name: str


# class GroupMemberResponse(BaseModel):
#     group_member_id: int
#     group_id: int
#     user_id : int
#     role_id: Optional[int] = None
#     status: str
#     created_at: datetime 
#     updated_at: datetime

#     class Config:
#         from_attributes = True

class BlogResponse(BaseModel):
    blog_id: int 
    user_id: int 
    group_id: int
    title: str
    content: str
    is_public: bool
    status: str
    created_at: datetime
    updated_at: datetime
    owner: UserOut
    group: GroupResponse
    class Config:
        from_attributes = True

class BlogCreate(BaseModel):
    title: str
    content: str
    is_public: bool

class ReactionResponse(BaseModel):
    reaction_id: int
    user_id: int
    blog_id: int
    reaction_type: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class ReactionCreate(BaseModel):
    reaction_type: str

    class Config:
        from_attributes = True

class CommentResponse(BaseModel):
    comment_id: int
    blog_id: int
    user_id: int
    parent_comment_id: Optional[int] = None
    content: str

    class Config:
        from_attributes = True

class CommentOfPostCreate(BaseModel):
    content: str

class CommentOfMemberCreate(BaseModel):
    content: str
    parent_comment_id: int

class RoleResponse(BaseModel):
    role_id: Optional[int] = None
    role_name: Optional[str] = None

class GroupMemberResponse(BaseModel):
    group_id: int
    user_id: int
    role_id: Optional[int] = None
    status: str
    user: UserOut
    group: GroupResponse
    role: Optional[RoleResponse] = None
