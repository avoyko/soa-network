import pytest
from datetime import datetime
import time

from app.models import Post, Tag
from app.exceptions import NotFoundError, PermissionDeniedError, ValidationError



def test_create_post(posts_service, db_session):
    unique_id = int(time.time())
    title = f"Test Post {unique_id}"
    description = "Test description"
    creator_id = "user-123"
    is_private = False
    tags = [f"tag-{unique_id}-1", f"tag-{unique_id}-2"]

    post = posts_service.create_post(
        title=title,
        description=description,
        creator_id=creator_id,
        is_private=is_private,
        tags=tags,
    )

    assert post is not None
    assert post.id is not None
    assert post.title == title
    assert post.description == description
    assert post.creator_id == creator_id
    assert post.is_private == is_private
    assert len(post.tags) == 2
    assert post.tags[0].name in tags
    assert post.tags[1].name in tags

    db_post = db_session.query(Post).filter(Post.id == post.id).first()
    assert db_post is not None
    assert db_post.title == title

    db_session.delete(post)
    for tag in post.tags:
        db_session.delete(tag)
    db_session.commit()


def test_create_post_validation_error(posts_service):
    with pytest.raises(ValidationError) as exc_info:
        posts_service.create_post(
            title="",
            description="Test description",
            creator_id="user-123",
            is_private=False,
            tags=["tag1"],
        )
    assert "Title and description are required" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        posts_service.create_post(
            title="Test Title",
            description="",
            creator_id="user-123",
            is_private=False,
            tags=["tag1"],
        )
    assert "Title and description are required" in str(exc_info.value)


def test_get_post(posts_service, sample_post):
    post = posts_service.get_post(
        post_id=sample_post.id, requester_id=sample_post.creator_id
    )

    assert post is not None
    assert post.id == sample_post.id
    assert post.title == sample_post.title
    assert post.description == sample_post.description
    assert post.creator_id == sample_post.creator_id


def test_get_post_not_found(posts_service):

    with pytest.raises(NotFoundError) as exc_info:
        posts_service.get_post(post_id="non-existent-id", requester_id="user-123")
    assert "Post with ID non-existent-id not found" in str(exc_info.value)


def test_get_private_post_by_creator(posts_service, private_post):

    post = posts_service.get_post(
        post_id=private_post.id, requester_id=private_post.creator_id
    )

    assert post is not None
    assert post.id == private_post.id
    assert post.is_private is True


def test_get_private_post_by_non_creator(posts_service, private_post):
    with pytest.raises(PermissionDeniedError) as exc_info:
        posts_service.get_post(post_id=private_post.id, requester_id="different-user")
    assert "You don't have permission to view this post" in str(exc_info.value)


def test_update_post(posts_service, sample_post, db_session):

    original_updated_at = sample_post.updated_at

    time.sleep(1)

    new_title = "Updated Title"
    new_description = "Updated description"
    new_is_private = True
    new_tags = ["new-tag-1", "new-tag-2"]

    updated_post = posts_service.update_post(
        post_id=sample_post.id,
        updater_id=sample_post.creator_id,
        title=new_title,
        description=new_description,
        is_private=new_is_private,
        tags=new_tags,
    )

    assert updated_post.id == sample_post.id
    assert updated_post.title == new_title
    assert updated_post.description == new_description
    assert updated_post.is_private == new_is_private
    assert len(updated_post.tags) == 2
    assert updated_post.tags[0].name in new_tags
    assert updated_post.tags[1].name in new_tags
    assert updated_post.updated_at > original_updated_at

    db_post = db_session.query(Post).filter(Post.id == sample_post.id).first()
    assert db_post.title == new_title
    assert db_post.is_private == new_is_private

    for tag in updated_post.tags:
        db_session.query(Tag).filter(Tag.name == tag.name).delete()
    db_session.commit()


def test_update_post_partial(posts_service, sample_post):
    original_description = sample_post.description
    original_is_private = sample_post.is_private
    original_tags = sample_post.tags

    new_title = "Only Title Updated"

    updated_post = posts_service.update_post(
        post_id=sample_post.id, updater_id=sample_post.creator_id, title=new_title
    )

    assert updated_post.title == new_title
    assert updated_post.description == original_description
    assert updated_post.is_private == original_is_private
    assert updated_post.tags == original_tags


def test_update_post_not_found(posts_service):
    with pytest.raises(NotFoundError) as exc_info:
        posts_service.update_post(
            post_id="non-existent-id", updater_id="user-123", title="New Title"
        )
    assert "Post with ID non-existent-id not found" in str(exc_info.value)


def test_update_post_by_non_creator(posts_service, sample_post):
    with pytest.raises(PermissionDeniedError) as exc_info:
        posts_service.update_post(
            post_id=sample_post.id, updater_id="different-user", title="New Title"
        )
    assert "Only the creator can update the post" in str(exc_info.value)


def test_delete_post(posts_service, sample_post, db_session):

    post_id = sample_post.id

    posts_service.delete_post(post_id=post_id, deleter_id=sample_post.creator_id)

    deleted_post = db_session.query(Post).filter(Post.id == post_id).first()
    assert deleted_post is None


def test_delete_post_not_found(posts_service):

    with pytest.raises(NotFoundError) as exc_info:
        posts_service.delete_post(post_id="non-existent-id", deleter_id="user-123")
    assert "Post with ID non-existent-id not found" in str(exc_info.value)


def test_delete_post_by_non_creator(posts_service, sample_post):

    with pytest.raises(PermissionDeniedError) as exc_info:
        posts_service.delete_post(post_id=sample_post.id, deleter_id="different-user")
    assert "Only the creator can delete the post" in str(exc_info.value)


def test_list_posts(posts_service, sample_post, db_session):

    posts = [sample_post]

    for i in range(3):
        post = Post(
            title=f"List Test Post {i}",
            description=f"Description {i}",
            creator_id="test-user-id",
            is_private=False,
        )
        db_session.add(post)
        posts.append(post)

    db_session.commit()

    try:

        page = 1
        page_size = 2
        result_posts, total_count, result_page, result_page_size = (
            posts_service.list_posts(
                page=page, page_size=page_size, viewer_id="test-user-id"
            )
        )

        assert len(result_posts) == 2
        assert total_count >= 4
        assert result_page == page
        assert result_page_size == page_size

        page = 2
        result_posts, total_count, result_page, result_page_size = (
            posts_service.list_posts(
                page=page, page_size=page_size, viewer_id="test-user-id"
            )
        )

        assert len(result_posts) > 0
        assert result_page == page
        assert result_page_size == page_size

    finally:

        for post in posts[1:]:
            db_session.delete(post)
        db_session.commit()


def test_list_posts_with_private(posts_service, sample_post, private_post, db_session):
    result_posts, total_count, _, _ = posts_service.list_posts(
        page=1, page_size=10, viewer_id="test-user-id"
    )

    assert len(result_posts) >= 2
    post_ids = [post.id for post in result_posts]
    assert sample_post.id in post_ids
    assert private_post.id in post_ids

    result_posts, total_count, _, _ = posts_service.list_posts(
        page=1, page_size=10, viewer_id="different-user"
    )

    post_ids = [post.id for post in result_posts]
    assert sample_post.id in post_ids
    assert private_post.id not in post_ids


def test_list_posts_invalid_parameters(posts_service):
    with pytest.raises(ValidationError) as exc_info:
        posts_service.list_posts(page=-1, page_size=10, viewer_id="user-123")
    assert "Page and page_size must be positive integers" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        posts_service.list_posts(page=1, page_size=0, viewer_id="user-123")
    assert "Page and page_size must be positive integers" in str(exc_info.value)


def test_get_or_create_tags(posts_service, db_session):
    unique_prefix = f"test-{int(time.time())}"
    tag_names = [f"{unique_prefix}-tag1", f"{unique_prefix}-tag2"]

    tags = posts_service._get_or_create_tags(tag_names)

    assert len(tags) == 2
    assert tags[0].name == tag_names[0]
    assert tags[1].name == tag_names[1]

    db_tags = db_session.query(Tag).filter(Tag.name.in_(tag_names)).all()
    assert len(db_tags) == 2

    second_tags = posts_service._get_or_create_tags(tag_names)

    assert len(second_tags) == 2
    assert second_tags[0].id == tags[0].id
    assert second_tags[1].id == tags[1].id

    # Очистка
    for tag in tags:
        db_session.delete(tag)
    db_session.commit()


def test_post_to_proto(posts_service, sample_post):
    proto_post = posts_service._post_to_proto(sample_post)

    assert proto_post.id == sample_post.id
    assert proto_post.title == sample_post.title
    assert proto_post.description == sample_post.description
    assert proto_post.creator_id == sample_post.creator_id
    assert proto_post.is_private == sample_post.is_private

    assert len(proto_post.tags) == len(sample_post.tags)
    assert proto_post.tags[0] == sample_post.tags[0].name

    assert proto_post.created_at.ToDatetime().date() == sample_post.created_at.date()
    assert proto_post.updated_at.ToDatetime().date() == sample_post.updated_at.date()
