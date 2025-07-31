import logging

from fastapi import APIRouter, HTTPException

from ..models.observation import Observation

logger = logging.getLogger(__name__)


router = APIRouter()

# In-memory "database"
observations_db = []


@router.post("/observations")
async def create_observation(observation: Observation):
    # validate the observation fields
    if observation.resourceType != "Observation":
        raise HTTPException(status_code=400, detail="resourceType must be 'Observation'")

    if not observation.subject or not observation.subject.reference.startswith("Patient/"):
        raise HTTPException(status_code=400, detail="subject.reference must start with 'Patient/'")

    if not observation.code or not observation.code.coding:
        raise HTTPException(status_code=400, detail="code.coding must not be empty")

    if not observation.code.coding[0].code:
        raise HTTPException(status_code=400, detail="code.coding[0].code is required")

    if not observation.valueQuantity or observation.valueQuantity.value is None:
        raise HTTPException(status_code=400, detail="valueQuantity.value is required")

    observations_db.append(observation)

    return {"message": "Observation stored successfully", "id": observation.id}
