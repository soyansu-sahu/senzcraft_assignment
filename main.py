import logging
import uvicorn

from fastapi import FastAPI
from routers import api


logger = logging.getLogger("uvicorn.error")

app = FastAPI()
app.include_router(api.router)


if __name__ == '__main__':
    logger.info("Starting FastAPI for senzcraft")
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
