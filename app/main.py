import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import routes

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="FHIR Mini Aggregator")

app.include_router(routes.router)

# Quick development fix to allow requests from any origin so that React app can access the endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
