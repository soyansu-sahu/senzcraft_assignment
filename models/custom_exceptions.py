import http
import logging
from fastapi.responses import JSONResponse


class ErrorResponse:
    message: str
    def __init__(self, error=None):
        self.error = error


class ApplicationException(Exception):

    def __init__(self, error="application exception occurred", status_code=http.HTTPStatus.BAD_REQUEST):
        self.error = error
        self.status_code = status_code
        super().__init__(self.error)

    def __str__(self):
        return str(self.error)
    
    def response(self):
        error_response = ErrorResponse(self.error)
        return JSONResponse(
            content=error_response.__dict__,
            status_code=self.status_code
        )


class GlobalException(Exception):

    def __init__(self, exception: Exception, status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR):
        self.error = exception
        self.status_code = status_code
        logging.exception({
            "context": "global-exception",
            "error_type": "global exception", 
            "error": self.error
        })
        super().__init__(self.error)

    def __str__(self):
        return str(self.error)
    
    def response(self):
        error_response = ErrorResponse(self.error)
        return JSONResponse(
            content=error_response.__dict__,
            status_code=self.status_code
        )
