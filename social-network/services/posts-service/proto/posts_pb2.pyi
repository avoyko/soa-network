from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreatePostRequest(_message.Message):
    __slots__ = ("title", "description", "creator_id", "is_private", "tags")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CREATOR_ID_FIELD_NUMBER: _ClassVar[int]
    IS_PRIVATE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    creator_id: str
    is_private: bool
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ..., creator_id: _Optional[str] = ..., is_private: bool = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class GetPostRequest(_message.Message):
    __slots__ = ("id", "requester_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    REQUESTER_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    requester_id: str
    def __init__(self, id: _Optional[str] = ..., requester_id: _Optional[str] = ...) -> None: ...

class UpdatePostRequest(_message.Message):
    __slots__ = ("id", "title", "description", "is_private", "tags", "updater_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IS_PRIVATE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    UPDATER_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    description: str
    is_private: bool
    tags: _containers.RepeatedScalarFieldContainer[str]
    updater_id: str
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., is_private: bool = ..., tags: _Optional[_Iterable[str]] = ..., updater_id: _Optional[str] = ...) -> None: ...

class DeletePostRequest(_message.Message):
    __slots__ = ("id", "deleter_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    DELETER_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    deleter_id: str
    def __init__(self, id: _Optional[str] = ..., deleter_id: _Optional[str] = ...) -> None: ...

class PostResponse(_message.Message):
    __slots__ = ("id", "title", "description", "creator_id", "created_at", "updated_at", "is_private", "tags")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CREATOR_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    IS_PRIVATE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    description: str
    creator_id: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    is_private: bool
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., creator_id: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., is_private: bool = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class ListPostsRequest(_message.Message):
    __slots__ = ("page", "page_size", "viewer_id")
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    VIEWER_ID_FIELD_NUMBER: _ClassVar[int]
    page: int
    page_size: int
    viewer_id: str
    def __init__(self, page: _Optional[int] = ..., page_size: _Optional[int] = ..., viewer_id: _Optional[str] = ...) -> None: ...

class ListPostsResponse(_message.Message):
    __slots__ = ("posts", "total_count", "page", "page_size")
    POSTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    posts: _containers.RepeatedCompositeFieldContainer[PostResponse]
    total_count: int
    page: int
    page_size: int
    def __init__(self, posts: _Optional[_Iterable[_Union[PostResponse, _Mapping]]] = ..., total_count: _Optional[int] = ..., page: _Optional[int] = ..., page_size: _Optional[int] = ...) -> None: ...

class Error(_message.Message):
    __slots__ = ("message", "code")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    message: str
    code: int
    def __init__(self, message: _Optional[str] = ..., code: _Optional[int] = ...) -> None: ...
