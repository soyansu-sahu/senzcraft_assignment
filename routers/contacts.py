from fastapi import APIRouter
from fastapi.responses import JSONResponse
from http import HTTPStatus

from controllers import contacts


router = APIRouter(prefix="/contacts")


@router.get("/v1/ping")
def ping():
    data = contacts.get_ping()
    return JSONResponse(content=data, status_code=HTTPStatus.OK)
