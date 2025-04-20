import pytest
import pytest_asyncio
import asyncio
import grpc
import time
from google.protobuf.empty_pb2 import Empty
from proto import posts_pb2


@pytest.mark.asyncio
async def test_grpc_create_post(posts_stub):

    try:

        unique_id = int(time.time())
        title = f"gRPC Test Post {unique_id}"
        description = f"gRPC test description {unique_id}"
        creator_id = "grpc-test-user"
        tags = [f"grpc-tag-{unique_id}-1", f"grpc-tag-{unique_id}-2"]

        request = posts_pb2.CreatePostRequest(
            title=title,
            description=description,
            creator_id=creator_id,
            is_private=False,
            tags=tags,
        )

        response = await posts_stub.CreatePost(request)

        assert response.id is not None
        assert response.title == title
        assert response.description == description
        assert response.creator_id == creator_id
        assert response.is_private is False
        assert set(response.tags) == set(tags)

        return response.id

    except grpc.RpcError as e:
        pytest.fail(f"gRPC error: {e.code()}: {e.details()}")


@pytest.mark.asyncio
async def test_grpc_get_post(posts_stub):

    try:

        post_id = await test_grpc_create_post(posts_stub)

        request = posts_pb2.GetPostRequest(
            id=post_id,
            requester_id="grpc-test-user",
        )

        response = await posts_stub.GetPost(request)

        assert response.id == post_id
        assert "gRPC Test Post" in response.title
        assert "grpc-test-user" == response.creator_id

    except grpc.RpcError as e:

        pytest.fail(f"gRPC error: {e.code()}: {e.details()}")


@pytest.mark.asyncio
async def test_grpc_update_post(posts_stub):
   
    try:

        post_id = await test_grpc_create_post(posts_stub)

        get_request = posts_pb2.GetPostRequest(
            id=post_id, requester_id="grpc-test-user"
        )
        original_post = await posts_stub.GetPost(get_request)

        new_title = f"Updated gRPC Post {int(time.time())}"
        new_description = f"Updated description {int(time.time())}"
        new_tags = [f"updated-tag-{int(time.time())}"]

        update_request = posts_pb2.UpdatePostRequest(
            id=post_id,
            title=new_title,
            description=new_description,
            is_private=True,
            tags=new_tags,
            updater_id="grpc-test-user",
        )

        response = await posts_stub.UpdatePost(update_request)

        assert response.id == post_id
        assert response.title == new_title
        assert response.description == new_description
        assert response.is_private is True
        assert set(response.tags) == set(new_tags)

        assert response.updated_at.seconds >= original_post.updated_at.seconds

    except grpc.RpcError as e:

        pytest.fail(f"gRPC error: {e.code()}: {e.details()}")


@pytest.mark.asyncio
async def test_grpc_update_post_unauthorized(posts_stub):

    post_id = await test_grpc_create_post(posts_stub)

    update_request = posts_pb2.UpdatePostRequest(
        id=post_id,
        title="Unauthorized Update",
        updater_id="different-user",
    )

    try:
        await posts_stub.UpdatePost(update_request)
        pytest.fail("Expected PERMISSION_DENIED error, but no error was raised")
    except grpc.RpcError as e:

        assert e.code() == grpc.StatusCode.PERMISSION_DENIED
        assert "Only the creator can update the post" in e.details()


@pytest.mark.asyncio
async def test_grpc_delete_post(posts_stub):
    try:

        post_id = await test_grpc_create_post(posts_stub)

        delete_request = posts_pb2.DeletePostRequest(
            id=post_id,
            deleter_id="grpc-test-user",
        )

        response = await posts_stub.DeletePost(delete_request)
        assert isinstance(response, Empty)

        get_request = posts_pb2.GetPostRequest(
            id=post_id, requester_id="grpc-test-user"
        )

        try:
            await posts_stub.GetPost(get_request)
            pytest.fail("Expected NOT_FOUND error, but no error was raised")
        except grpc.RpcError as e:

            assert e.code() == grpc.StatusCode.NOT_FOUND
            assert f"Post with ID {post_id} not found" in e.details()

    except grpc.RpcError as e:

        if e.code() != grpc.StatusCode.NOT_FOUND:
            pytest.fail(f"Unexpected gRPC error: {e.code()}: {e.details()}")


@pytest.mark.asyncio
async def test_grpc_list_posts(posts_stub):

    try:

        for i in range(3):
            unique_id = int(time.time()) + i
            await asyncio.sleep(0.1)

            request = posts_pb2.CreatePostRequest(
                title=f"List Test Post {unique_id}",
                description=f"List test description {unique_id}",
                creator_id="grpc-list-test-user",
                is_private=False,
                tags=[f"list-tag-{unique_id}"],
            )
            await posts_stub.CreatePost(request)

        private_request = posts_pb2.CreatePostRequest(
            title=f"Private Post {int(time.time())}",
            description="Private post for list test",
            creator_id="grpc-list-test-user",
            is_private=True,
            tags=["private-tag"],
        )
        await posts_stub.CreatePost(private_request)

        list_request = posts_pb2.ListPostsRequest(
            page=1, page_size=10, viewer_id="grpc-list-test-user"
        )

        response = await posts_stub.ListPosts(list_request)

        assert response.total_count >= 4
        assert len(response.posts) >= 4
        assert response.page == 1
        assert response.page_size == 10

        list_request_other = posts_pb2.ListPostsRequest(
            page=1, page_size=10, viewer_id="different-usr"
        )

        response_other = await posts_stub.ListPosts(list_request_other)

        assert response_other.posts != response.posts

    except grpc.RpcError as e:
        pytest.fail(f"gRPC error: {e.code()}: {e.details()}")
