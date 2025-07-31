from fastapi import APIRouter
from ..models.observation import Observation


router = APIRouter()

# In-memory "database"
observations_db = []


@router.get("/")
def root():
    return {"message": "FHIR Mini Aggregator running"}


@router.post("/observations")
def create_observation(observation: Observation):
    observations_db.append(observation)
    return {"message": "Observation stored successfully", "id": observation.id}
