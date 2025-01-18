from fastapi import HTTPException, status
from typing import Optional, Dict, Any

class BookAPIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class NotFoundError(BookAPIException):
    def __init__(self, resource: str, resource_id: Any):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} with id {resource_id} not found"
        )

class AuthenticationError(BookAPIException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class ConflictError(BookAPIException):
    def __init__(self, resource: str, detail: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{resource} conflict: {detail}"
        )

class DuplicateBookError(ConflictError):
    def __init__(self, title: str):
        super().__init__("Book", f"Book with title '{title}' already exists")