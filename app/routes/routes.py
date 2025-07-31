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


@router.get("/patients/{patient_id}/metrics")
def get_patient_metrics(patient_id: str):
    # filter observations belonging to this patient
    patient_observations = [
        obs for obs in observations_db
        if obs.subject.reference == f"Patient/{patient_id}"
    ]

    if not patient_observations:
        raise HTTPException(status_code=404, detail="No observations found for this patient")

    # observation count
    observation_count = len(patient_observations)

    # latest observation (by effectiveDateTime)
    latest_obs = max(patient_observations, key=lambda o: o.effectiveDateTime)

    # calculate average value grouped by LOINC code
    sums_by_code = {}
    counts_by_code = {}

    for obs in patient_observations:
        code = obs.code.coding[0].code  # Get LOINC code
        value = obs.valueQuantity.value
        sums_by_code[code] = sums_by_code.get(code, 0) + value
        counts_by_code[code] = counts_by_code.get(code, 0) + 1

    average_by_code = {
        code: sums_by_code[code] / counts_by_code[code] for code in sums_by_code
    }

    return {
        "patientId": patient_id,
        "observationCount": observation_count,
        "latest": latest_obs.dict(),
        "averageByCode": average_by_code
    }
