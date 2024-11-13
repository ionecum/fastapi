from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime, timezone

Base = declarative_base()

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False)

    @hybrid_property
    def deleted(self):
        return self.is_deleted
    
    @deleted.setter
    def deleted(self, value):
        self.is_deleted = value
    

class TimestampMixin:
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))


class User(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    #posts = relationship("Post", back_populates="author")


class Post(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    #author = relationship("User", back_populates="posts")
    #comments = relationship("Comment", back_populates="post")
    #tags = relationship("Tag", secondary="post_tags", back_populates="posts")


class Comment(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

    #post = relationship("Post", back_populates="comments")


class Tag(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    #posts = relationship("Post", secondary="post_tags", back_populates="tags")


""" class PostTag(Base):
    __tablename__ = "post_tags"
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True) """
