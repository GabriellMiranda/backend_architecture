from fastapi import HTTPException, status
from typing import Dict, Any


class Conflict(HTTPException):
    def __init__(
            self, detail: str = 'Error of integrity', headers: Dict[str, Any] = None
    ) -> None:
        super().__init__(status.HTTP_409_CONFLICT, detail=detail, headers=headers)
