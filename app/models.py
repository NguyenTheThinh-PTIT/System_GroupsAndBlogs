from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # group_members = relationship("GroupMember", back_populates="user")

class Group(Base):
    __tablename__ = "groups"

    group_id = Column(Integer, primary_key=True, nullable=False)
    group_name = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # members = relationship("GroupMember", back_populates="group")

class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, nullable=False)
    role_name = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # group_members = relationship("GroupMember", back_populates="role")

class Group_Member(Base):
    __tablename__ = "group_members"

    group_member_id = Column(Integer, primary_key=True, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.group_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id", ondelete="CASCADE"), nullable=True)
    status = Column(String, default='pending')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    group = relationship("Group")
    user = relationship("User")
    role = relationship("Role")

    

class Blog(Base):
    __tablename__ = "blogs"

    blog_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.group_id', ondelete="CASCADE"), nullable=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_public = Column(Boolean, default=False)
    status = Column(String, default='pending')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner = relationship("User")
    group = relationship("Group")

class Reaction(Base): 
    __tablename__ = 'reactions'

    reaction_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    blog_id = Column(Integer, ForeignKey('blogs.blog_id', ondelete="CASCADE"), nullable=False)
    reaction_type = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # owner = relationship("User")
    # blog = relationship("Blog")

class Comment(Base):
    __tablename__ = 'comments'
    
    comment_id = Column(Integer, primary_key=True, nullable=False)
    blog_id = Column(Integer, ForeignKey('blogs.blog_id', ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    parent_comment_id = Column(Integer, ForeignKey('comments.comment_id'), nullable=True)
    content = Column(String, nullable=False)
    # blog = relationship("Blog")
    # user = relationship("User")
    # parent_comment = relationship("Comment")