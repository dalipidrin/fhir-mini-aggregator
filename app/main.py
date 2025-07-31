from fastapi import FastAPI
from .routes import router

app = FastAPI(title="FHIR Mini Aggregator")

app.include_router(router)
