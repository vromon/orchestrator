from pydantic import BaseModel
class TripSchema(BaseModel):
    user_query:str
class ItinerarySchema(BaseModel):
    itinerary:str