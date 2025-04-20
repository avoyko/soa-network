from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Post(_message.Message):
    __slots__ = ("id", "title", "description", "username", "created_at", "updated_at", "is_private", "tags")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    IS_PRIVATE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    description: str
    username: str
    created_at: str
    updated_at: str
    is_private: bool
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., username: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., is_private: bool = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class CreatePostRequest(_message.Message):
    __slots__ = ("title", "description", "username", "is_private", "tags")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    IS_PRIVATE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    username: str
    is_private: bool
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ..., username: _Optional[str] = ..., is_private: bool = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class GetPostRequest(_message.Message):
    __slots__ = ("post_id", "username")
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    username: str
    def __init__(self, post_id: _Optional[int] = ..., username: _Optional[str] = ...) -> None: ...

class UpdatePostRequest(_message.Message):
    __slots__ = ("post_id", "username", "title", "description", "is_private", "tags")
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IS_PRIVATE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    username: str
    title: str
    description: str
    is_private: bool
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, post_id: _Optional[int] = ..., username: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., is_private: bool = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class DeletePostRequest(_message.Message):
    __slots__ = ("post_id", "username")
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    username: str
    def __init__(self, post_id: _Optional[int] = ..., username: _Optional[str] = ...) -> None: ...

class DeletePostResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class ListPostsRequest(_message.Message):
    __slots__ = ("page", "page_size", "username", "tag")
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    page: int
    page_size: int
    username: str
    tag: str
    def __init__(self, page: _Optional[int] = ..., page_size: _Optional[int] = ..., username: _Optional[str] = ..., tag: _Optional[str] = ...) -> None: ...

class ListPostsResponse(_message.Message):
    __slots__ = ("posts", "total", "page", "page_size", "pages")
    POSTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGES_FIELD_NUMBER: _ClassVar[int]
    posts: _containers.RepeatedCompositeFieldContainer[Post]
    total: int
    page: int
    page_size: int
    pages: int
    def __init__(self, posts: _Optional[_Iterable[_Union[Post, _Mapping]]] = ..., total: _Optional[int] = ..., page: _Optional[int] = ..., page_size: _Optional[int] = ..., pages: _Optional[int] = ...) -> None: ...

class PostResponse(_message.Message):
    __slots__ = ("post",)
    POST_FIELD_NUMBER: _ClassVar[int]
    post: Post
    def __init__(self, post: _Optional[_Union[Post, _Mapping]] = ...) -> None: ...
