from fastapi import FastAPI
from app.routes import routes
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="FHIR Mini Aggregator")

app.include_router(routes.router)
