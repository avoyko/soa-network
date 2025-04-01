from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4

Base = declarative_base()

post_tags_association = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", String, ForeignKey("posts.id")),
    Column("tag_id", String, ForeignKey("tags.id")),
)


class Post(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    creator_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_private = Column(Boolean, default=False)

    tags = relationship("Tag", secondary=post_tags_association, backref="posts")

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}')>"


class Tag(Base):
    __tablename__ = "tags"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}')>"
