from app.core.exceptions.base import ApiException


class NotFoundError(ApiException):
    __slots__ = ()

    def __init__(self,  detail: str ="Resource not found",**kwargs):
        super().__init__(status_code=404, detail=detail, error_code="NOT_FOUND", **kwargs)

class ValidationError(ApiException):
    __slots__ = ()
    def __init__(self, detail: str = "Validation failed", **kwargs):
        super().__init__(status_code=422, detail=detail, error_code="VALIDATION_ERROR", **kwargs)

class DatabaseError(ApiException):
    __slots__ = ()
    def __init__(self, detail: str = "Database operation failed", **kwargs):
        super().__init__(status_code=500, detail=detail, error_code="DATABASE_ERROR", **kwargs)

class UnauthorizedError(ApiException):
    __slots__ = ()
    def __init__(self, detail: str = "Unauthorized access", **kwargs):
        super().__init__(status_code=401, detail=detail, error_code="UNAUTHORIZED", **kwargs)