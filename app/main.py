from fastapi import FastAPI
from app.routes.routes import router

app = FastAPI(title="FHIR Mini Aggregator")

app.include_router(router)
