from fastapi import FastAPI,Request, HTTPException
from fastapi.responses import JSONResponse

def register_exception_handlers(app:FastAPI):
    @app.exception_handler(Exception)
    def global_exception_handler(request:Request,exc:Exception):
        print(f"server error:{exc}")
        return JSONResponse(
            status_code=500,
            content={
                "success":False,
                "message":"Internal server error"
            }
        )
    @app.exception_handler(HTTPException)
    def http_exception_handler(request:Request,exc:HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success":False,
                "message":exc.detail
            }
        )
