from upstash_redis.asyncio import Redis
from app.config import settings

def get_redis_cient()->Redis:
    return Redis(
 url=settings.UPSTASH_REDIS_REST_URL,
 token=settings.UPSTASH_REDIS_REST_TOKEN
)
# import redis.asyncio as redis

# from app.config import settings


# def get_redis_cient():

#     return redis.from_url(
#         settings.REDIS_URL,
#         decode_responses=True
#     )