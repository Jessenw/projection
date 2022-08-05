from fastapi import FastAPI
from routers import groupbuys, interest_checks

app = FastAPI()

app.include_router(groupbuys.router)
app.include_router(interest_checks.router)
