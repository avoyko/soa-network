from sqlalchemy.orm import Session
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from app.models import Post, Tag
from app.exceptions import NotFoundError, PermissionDeniedError, ValidationError
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class PostsService:
    def __init__(self, db: Session):
        self.db = db

    def _post_to_proto(self, post: Post):
        from posts_pb2 import PostResponse

        created_at = Timestamp()
        created_at.FromDatetime(post.created_at)

        updated_at = Timestamp()
        updated_at.FromDatetime(post.updated_at)

        return PostResponse(
            id=post.id,
            title=post.title,
            description=post.description,
            creator_id=post.creator_id,
            created_at=created_at,
            updated_at=updated_at,
            is_private=post.is_private,
            tags=[tag.name for tag in post.tags],
        )

    def _get_or_create_tags(self, tag_names: List[str]) -> List[Tag]:
        tags = []
        for tag_name in tag_names:
            tag = self.db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                self.db.add(tag)
            tags.append(tag)
        return tags

    def create_post(
        self,
        title: str,
        description: str,
        creator_id: str,
        is_private: bool,
        tags: List[str],
    ) -> Post:
        if not title or not description:
            raise ValidationError("Title and description are required")

        post = Post(
            title=title,
            description=description,
            creator_id=creator_id,
            is_private=is_private,
        )

        if tags:
            post.tags = self._get_or_create_tags(tags)

        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)

        logger.info(f"Created post with ID: {post.id}")
        return post

    def get_post(self, post_id: str, requester_id: str) -> Post:

        post = self.db.query(Post).filter(Post.id == post_id).first()

        if not post:
            raise NotFoundError(f"Post with ID {post_id} not found")

        if post.is_private and post.creator_id != requester_id:
            raise PermissionDeniedError("You don't have permission to view this post")

        return post

    def update_post(
        self,
        post_id: str,
        updater_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        is_private: Optional[bool] = None,
        tags: Optional[List[str]] = None,
    ) -> Post:

        post = self.db.query(Post).filter(Post.id == post_id).first()

        if not post:
            raise NotFoundError(f"Post with ID {post_id} not found")

        if post.creator_id != updater_id:
            raise PermissionDeniedError("Only the creator can update the post")

        if title is not None:
            post.title = title
        if description is not None:
            post.description = description
        if is_private is not None:
            post.is_private = is_private
        if tags is not None:
            post.tags = self._get_or_create_tags(tags)

        post.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(post)

        logger.info(f"Updated post with ID: {post.id}")
        return post

    def delete_post(self, post_id: str, deleter_id: str) -> None:

        post = self.db.query(Post).filter(Post.id == post_id).first()

        if not post:
            raise NotFoundError(f"Post with ID {post_id} not found")

        if post.creator_id != deleter_id:
            raise PermissionDeniedError("Only the creator can delete the post")

        self.db.delete(post)
        self.db.commit()

        logger.info(f"Deleted post with ID: {post.id}")

    def list_posts(self, page: int, page_size: int, viewer_id: str) -> tuple:

        if page < 1 or page_size < 1:
            raise ValidationError("Page and page_size must be positive integers")

        query = self.db.query(Post)

        query = query.filter(
            (Post.is_private == False) | (Post.creator_id == viewer_id)
        )

        total_count = query.count()

        offset = (page - 1) * page_size
        posts = (
            query.order_by(Post.created_at.desc()).offset(offset).limit(page_size).all()
        )

        return posts, total_count, page, page_size
