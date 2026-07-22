# from app.services import trip_service
# from fastapi import APIRouter
# from fastapi.responses import StreamingResponse
# from app.schemas.trip_schema import TripSchema
# trip_router=APIRouter(prefix="/trip")
# @trip_router.post("/generate")
# def create_trip_plan(trip_request:TripSchema):

#     # return trip_service.create_trip_plan(trip_request)

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.trip_schema import TripSchema
from app.services.trip_service import stream_trip

trip_router = APIRouter(prefix="/trip")


@trip_router.post("/generate")
async def create_trip_plan(trip_request: TripSchema):

    return StreamingResponse(
        stream_trip(trip_request),
        media_type="text/plain; charset=utf-8",
    )