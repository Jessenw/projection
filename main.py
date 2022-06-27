from fastapi import FastAPI
from routers import groupbuys, interest_checks


api = FastAPI()

api.include_router(groupbuys.router)
api.include_router(interest_checks.router)
