from fastapi import Request
from fastapi.responses import JSONResponse
from .exception_types import BookAPIException
from sqlalchemy.exc import SQLAlchemyError

async def book_exception_handler(request: Request, exc: BookAPIException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": str(exc.detail)
        },
        headers=exc.headers
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal database error occurred"
        }
    )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "An unexpected error occurred"
        }
    )

def register_exception_handlers(app):
    app.add_exception_handler(BookAPIException, book_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)