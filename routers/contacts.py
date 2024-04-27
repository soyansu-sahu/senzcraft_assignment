from fastapi import APIRouter
from fastapi.responses import JSONResponse
from http import HTTPStatus

from controllers import contacts

from fastapi import APIRouter, File, UploadFile, Request
from models.custom_exceptions import ApplicationException, GlobalException



router = APIRouter(prefix="/contacts")


@router.get("/v1/ping")
def ping():
    data = contacts.get_ping()
    return JSONResponse(content=data, status_code=HTTPStatus.OK)

@router.post("/v1/files")
async def create_file(file: UploadFile):
    """
    Uploads file for contacts
    """
    try:
        file_content = await file.read()
        print("[INFO]: filename: ", file.filename)
        resp, status = contacts.create_contacts_from_file(file_content)
    except ApplicationException as ae:
        print("[ERROR]: ae: ", ae)
        return ae.response()
    except GlobalException as ge:
        print("[ERROR]: ge: ", ge)
        return ge.response()
    
    return JSONResponse(content=resp, status_code=200)



@router.get("/v1/all")
async def detail():
    try:
        resp, status = contacts.read_all_contacts()
    except ApplicationException as ae:
        print("[ERROR]: ae: ", ae)
        return ae.response()
    except GlobalException as ge:
        print("[ERROR]: ge: ", ge)
        return ge.response()

    return JSONResponse(content={"data": resp}, status_code=status)
