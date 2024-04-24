from fastapi import APIRouter
from routers import contacts

router = APIRouter(prefix="/api-senzcraft")

router.include_router(contacts.router)
