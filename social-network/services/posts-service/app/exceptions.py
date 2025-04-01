from grpc import StatusCode

class PostServiceError(Exception):
    code = StatusCode.UNKNOWN
    message = "Unknown error occurred"
    
    def __init__(self, message=None):
        if message:
            self.message = message
        super().__init__(self.message)

class NotFoundError(PostServiceError):
    code = StatusCode.NOT_FOUND
    message = "Resource not found"

class PermissionDeniedError(PostServiceError):
    code = StatusCode.PERMISSION_DENIED
    message = "Permission denied"

class ValidationError(PostServiceError):
    code = StatusCode.INVALID_ARGUMENT
    message = "Validation error"

class InternalError(PostServiceError):
    code = StatusCode.INTERNAL
    message = "Internal server error"
