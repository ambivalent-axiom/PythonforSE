import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.exceptions import UserAlreadyExists, UserNotFound

logger = logging.getLogger(__name__)


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserNotFound)
    async def handle_user_not_found(request: Request, exc: UserNotFound):
        logger.error(f"Invalid user ID {exc.user_id} was requested")
        return JSONResponse(
            status_code=404,
            content="User doesn't exist",
        )

    @app.exception_handler(UserAlreadyExists)
    async def user_already_exists(request: Request, exc: UserAlreadyExists):
        logger.error(f"Tried to insert user that already exists")
        return JSONResponse(
            status_code=400,
            content="User already exists",
        )

    @app.exception_handler(IntegrityError)
    async def error_inserting_user(request: Request, exc: IntegrityError):
        logger.error(
            f"Encountered integrity error when inserting user: {str(exc)}"
        )  # here I am outputting the error msgs from sqlalchemy exc
        return JSONResponse(
            status_code=400,
            content="User conflicts with existing user",  # as an alternative, I can resturn a string version of exc - str(exc) in content, but it provides too much data for consumers, but goot for dev
        )

    return None
