from fastapi import FastAPI
from app.routers.trip_routes import trip_router
from app.routers.auth_router import auth_router
from app.routers.user_router import user_router
from app.middlewares.cors import register_cors
from app.middlewares.exception_handler import register_exception_handlers
# from app.database import Base, engine
app=FastAPI(title="AI Trip Planner Server")
# Base.metadata.create_all(engine)

register_cors(app)
register_exception_handlers(app)
@app.get("/")
def home():
    return{"status":"AI Trip Planner is Running"}
app.include_router(trip_router)
app.include_router(auth_router)
app.include_router(user_router)