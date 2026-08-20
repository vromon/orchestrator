# from app.schemas.trip_schema import TripSchema
# from app.ai.chains.trip_chain import stream_chain
# # def create_trip_plan(trip_request:TripSchema):
# #     return invoke_chain(trip_request.user_query)
from fastapi import  HTTPException, status
from app.schemas.trip_schema import TripSchema
from app.ai.chains.trip_chain import stream_chain
from app.caching.client import get_redis_cient
from supabase import create_client, Client
from app.supabase.client import get_supabase_client
from app.schemas.trip_schema import ItinerarySchema
import json
import time
import asyncio
import hashlib
import pybreaker
from app.utils.circuite_breaker import get_circuit_breaker
redis_client=get_redis_cient()
circuit_breaker=get_circuit_breaker()
async def stream_trip(trip_request: TripSchema):

    global g_uncached_time
    generalised=trip_request.user_query.lower().strip()
    cache_key=hashlib.sha256(
        generalised.encode()
    ).hexdigest()
    
    start_time=time.perf_counter()
    try:
        cached=None
        cached = await circuit_breaker.call_async(redis_client.get,cache_key)
    except pybreaker.CircuitBreakerError:
        print("Circuit is Open!")
    except Exception as e:
        print(f"Error getting redis data:{e}")
    
    try:
        if cached:

            cached_res = json.loads(cached)
            words=cached_res.split(".")

            for i,word in enumerate(words):

                chunk=word+" "if i<len(words)-1 else word
                yield chunk
                await asyncio.sleep(0.01)
 
            cached_time = time.perf_counter() - start_time
            print(f"Time spent at cache hit={cached_time:.4f} seconds")
            time_reduced=g_uncached_time-cached_time
            percentage_reduction=(time_reduced/g_uncached_time)*100
            print(f"Response time reduced by {percentage_reduction:.2f}%")
            return 
    except Exception as e:
        print(f"Error parsing cached JSON: {e}")
         

    
    cached_res=""

    async for chunk in stream_chain(trip_request.user_query):
            cached_res+=chunk
            yield chunk
        
    try:

        await circuit_breaker.call_async(redis_client.setex,cache_key,20,json.dumps(cached_res))
    
        uncached_time = time.perf_counter() - start_time
        g_uncached_time=uncached_time
        print(f"Time spent at cache miss={uncached_time:.4f} seconds")
    except pybreaker.CircuitBreakerError:
        print("Circuit is OPEN! Skipping Redis SET.")
    except Exception as e:
            print(f"Error saving data to redis: {e}")
    
        

       
        

supabase=get_supabase_client()
def save_itinerary(payload:ItinerarySchema):
    if not payload.itinerary:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No trip itinerary found to be saved"
        )

    response=supabase.table("itinerary").insert({"itinerary":payload.itinerary}).execute()
    return {"message":"Itinerary saved successfully",
    "data":response.data
}



