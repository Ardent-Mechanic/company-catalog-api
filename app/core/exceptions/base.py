from typing import Any, Optional


class ApiException(Exception):
    __slots__ = ("status_code", "detail", "headers", "error_code", "data")
    
    def __init__(
        self,
        *,
        status_code: int = 500,
        detail: str = "Internal server error",
        error_code: Optional[str] = None,
        headers: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
    ):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code
        self.headers = headers
        self.data = data

        super().__init__(detail)

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(status_code={self.status_code}, "
            f"detail={self.detail}, error_code={self.error_code})"
        )

    def to_dict(self) -> dict[str, Any]:
        response = {"detail": self.detail, "data": {}} 
        if self.error_code:
            response["error_code"] = self.error_code
        if self.data:
            response["data"] = self.data
        return response
    