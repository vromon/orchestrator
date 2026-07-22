# from app.schemas.trip_schema import TripSchema
# from app.ai.chains.trip_chain import stream_chain
# # def create_trip_plan(trip_request:TripSchema):
# #     return invoke_chain(trip_request.user_query)

from app.schemas.trip_schema import TripSchema
from app.ai.chains.trip_chain import stream_chain


async def stream_trip(body: TripSchema):

    async for chunk in stream_chain(body.user_query):
        yield chunk