import grpc
from concurrent import futures
import time
import logging
from sqlalchemy.orm import Session
import os

from app.database import engine, get_db, SessionLocal
from app.models import Base
from app.service import PostsService
from app.exceptions import PostServiceError

import posts_pb2
import posts_pb2_grpc

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


class PostsServiceServicer(posts_pb2_grpc.PostsServiceServicer):
    def __init__(self):
        pass

    def _get_db(self):
        return SessionLocal()

    def _handle_exceptions(self, context, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PostServiceError as e:
            context.set_code(e.code)
            context.set_details(e.message)
            logger.error(f"Service error: {e.message} (code: {e.code})")
            return None
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal server error: {str(e)}")
            logger.exception("Unexpected error")
            return None

    def CreatePost(self, request, context):
        db = self._get_db()
        try:
            service = PostsService(db)
            post = self._handle_exceptions(
                context,
                service.create_post,
                title=request.title,
                description=request.description,
                creator_id=request.creator_id,
                is_private=request.is_private,
                tags=list(request.tags),
            )

            if post:
                return service._post_to_proto(post)
            return posts_pb2.PostResponse()
        finally:
            db.close()

    def GetPost(self, request, context):
        db = self._get_db()
        try:
            service = PostsService(db)
            post = self._handle_exceptions(
                context,
                service.get_post,
                post_id=request.id,
                requester_id=request.requester_id,
            )

            if post:
                return service._post_to_proto(post)
            return posts_pb2.PostResponse()
        finally:
            db.close()

    def UpdatePost(self, request, context):
        db = self._get_db()
        try:
            service = PostsService(db)
            post = self._handle_exceptions(
                context,
                service.update_post,
                post_id=request.id,
                updater_id=request.updater_id,
                title=request.title if request.title else None,
                description=request.description if request.description else None,
                is_private=(
                    request.is_private if request.HasField("is_private") else None
                ),
                tags=list(request.tags) if request.tags else None,
            )

            if post:
                return service._post_to_proto(post)
            return posts_pb2.PostResponse()
        finally:
            db.close()

    def DeletePost(self, request, context):
        db = self._get_db()
        try:
            service = PostsService(db)
            success = self._handle_exceptions(
                context,
                service.delete_post,
                post_id=request.id,
                deleter_id=request.deleter_id,
            )

            if success is not None:
                return posts_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
            return posts_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        finally:
            db.close()

    def ListPosts(self, request, context):
        db = self._get_db()
        try:
            service = PostsService(db)
            result = self._handle_exceptions(
                context,
                service.list_posts,
                page=request.page,
                page_size=request.page_size,
                viewer_id=request.viewer_id,
            )

            if result:
                posts, total_count, page, page_size = result
                response = posts_pb2.ListPostsResponse(
                    total_count=total_count, page=page, page_size=page_size
                )
                for post in posts:
                    response.posts.append(service._post_to_proto(post))
                return response
            return posts_pb2.ListPostsResponse()
        finally:
            db.close()


def serve():

    Base.metadata.create_all(bind=engine)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    posts_pb2_grpc.add_PostsServiceServicer_to_server(PostsServiceServicer(), server)

    port = os.getenv("GRPC_PORT", "50051")
    server.add_insecure_port(f"[::]:{port}")
    server.start()

    logger.info(f"gRPC server started on port {port}")

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
        logger.info("Server stopped")


if __name__ == "__main__":
    serve()
