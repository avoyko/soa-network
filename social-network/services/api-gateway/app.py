from fastapi import FastAPI, Request, Response, HTTPException
import grpc
import httpx
import json
from fastapi.responses import JSONResponse

from proto import posts_pb2, posts_pb2_grpc

app = FastAPI(title="API Gateway")

USERS_SERVICE_URL = "http://users-service:8000"
POSTS_SERVICE_URL = "http://posts-service:50051"


@app.api_route("/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def users_proxy(request: Request, path: str):
    url = f"{USERS_SERVICE_URL}/{path}"
    client = httpx.AsyncClient()

    headers = {
        key: value for key, value in request.headers.items() if key.lower() != "host"
    }

    body = await request.body()

    response = await client.request(
        method=request.method,
        url=url,
        headers=headers,
        content=body,
    )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )


@app.api_route("/posts/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def posts_proxy(request: Request, path: str):
    channel = grpc.insecure_channel(POSTS_SERVICE_URL)
    client = posts_pb2_grpc.PostServiceStub(channel)

    try:
        request_body = await request.json() if request.method in ["POST", "PUT"] else {}

        if request.method == "POST" and not path:
            grpc_request = posts_pb2.CreatePostRequest(
                title=request_body.get("title", ""),
                description=request_body.get("description", ""),
                username=request_body.get("username", ""),
                is_private=request_body.get("is_private", False),
                tags=request_body.get("tags", []),
            )
            grpc_response = client.CreatePost(grpc_request)
            response_data = {
                "post": {
                    "id": grpc_response.post.id,
                    "title": grpc_response.post.title,
                    "description": grpc_response.post.description,
                    "username": grpc_response.post.username,
                    "created_at": grpc_response.post.created_at,
                    "updated_at": grpc_response.post.updated_at,
                    "is_private": grpc_response.post.is_private,
                    "tags": list(grpc_response.post.tags),
                }
            }

        elif request.method == "GET" and path.isdigit():
            post_id = int(path)
            query_params = dict(request.query_params)
            username = query_params.get("username", "")

            grpc_request = posts_pb2.GetPostRequest(post_id=post_id, username=username)
            grpc_response = client.GetPost(grpc_request)
            response_data = {
                "post": {
                    "id": grpc_response.post.id,
                    "title": grpc_response.post.title,
                    "description": grpc_response.post.description,
                    "username": grpc_response.post.username,
                    "created_at": grpc_response.post.created_at,
                    "updated_at": grpc_response.post.updated_at,
                    "is_private": grpc_response.post.is_private,
                    "tags": list(grpc_response.post.tags),
                }
            }

        elif request.method == "PUT" and path.isdigit():
            post_id = int(path)
            username = request_body.get("username", "")

            grpc_request = posts_pb2.UpdatePostRequest(
                post_id=post_id,
                username=username,
                title=request_body.get("title", ""),
                description=request_body.get("description", ""),
                is_private=request_body.get("is_private", False),
                tags=request_body.get("tags", []),
            )
            grpc_response = client.UpdatePost(grpc_request)
            response_data = {
                "post": {
                    "id": grpc_response.post.id,
                    "title": grpc_response.post.title,
                    "description": grpc_response.post.description,
                    "username": grpc_response.post.username,
                    "created_at": grpc_response.post.created_at,
                    "updated_at": grpc_response.post.updated_at,
                    "is_private": grpc_response.post.is_private,
                    "tags": list(grpc_response.post.tags),
                }
            }

        elif request.method == "DELETE" and path.isdigit():
            post_id = int(path)
            query_params = dict(request.query_params)
            username = query_params.get("username", "")

            grpc_request = posts_pb2.DeletePostRequest(
                post_id=post_id, username=username
            )
            grpc_response = client.DeletePost(grpc_request)
            response_data = {
                "success": grpc_response.success,
                "message": grpc_response.message,
            }

        elif request.method == "GET" and not path:
            query_params = dict(request.query_params)
            page = int(query_params.get("page", "1"))
            page_size = int(query_params.get("page_size", "10"))
            username = query_params.get("username", "")
            tag = query_params.get("tag", "")

            grpc_request = posts_pb2.ListPostsRequest(
                page=page, page_size=page_size, username=username, tag=tag
            )
            grpc_response = client.ListPosts(grpc_request)
            response_data = {
                "posts": [
                    {
                        "id": post.id,
                        "title": post.title,
                        "description": post.description,
                        "username": post.username,
                        "created_at": post.created_at,
                        "updated_at": post.updated_at,
                        "is_private": post.is_private,
                        "tags": list(post.tags),
                    }
                    for post in grpc_response.posts
                ],
                "total": grpc_response.total,
                "page": grpc_response.page,
                "page_size": grpc_response.page_size,
                "pages": grpc_response.pages,
            }

        else:
            return JSONResponse(status_code=404, content={"detail": "Route not found"})

        return JSONResponse(status_code=200, content=response_data)

    except grpc.RpcError as e:
        status_code = 404 if "not found" in e.details().lower() else 500
        return JSONResponse(
            status_code=status_code, content={"detail": f"gRPC error: {e.details()}"}
        )

    except json.JSONDecodeError:
        return JSONResponse(
            status_code=400, content={"detail": "Invalid JSON in request body"}
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Error: {str(e)}"})
