from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.services.auth import AuthService
from ..models.observation import Observation

router = APIRouter()

# In-memory "database"
observations_db = []


@router.post("/auth")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate user and issue a JWT access token.

    Accepts username and password via form data. If credentials match the hardcoded user ("user"/"pass"), returns a JWT bearer token with an
    expiration time. Otherwise, raises an HTTP 400 error.

    :param form_data: An instance of OAuth2PasswordRequestForm containing the username and password from the login form.
    :return: The access token and the token type ("bearer").
    """

    if form_data.username != "user" or form_data.password != "pass":
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = AuthService.create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/observations")
async def create_observation(observation: Observation, _: None = Depends(AuthService.verify_token)):
    """
    Create and store an Observation resource.

    This endpoint accepts an Observation object and performs validation on key fields. It requires authentication via a bearer token, which
    is verified by the `verify_token` dependency.

    Validations:
    - `resourceType` must be "Observation".
    - `subject.reference` must start with "Patient/".
    - `code.coding` list must not be empty and must include a `code`.
    - `valueQuantity.value` must be present.

    If validation passes, the observation is stored in memory.

    :param observation: The Observation resource to store.
    :param _: Parameter is used only to trigger token verification via dependency injection.
    :raise HTTPException: If any required fields are missing or invalid.
    :return: A success message and the ID of the stored Observation
    """

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
def get_patient_metrics(patient_id: str, _: None = Depends(AuthService.verify_token)):
    """
    Retrieve summary metrics for a patient's observations.

    This endpoint returns:
    - The number of observations recorded for the patient.
    - The latest observation based on `effectiveDateTime`.
    - The average value per observation code (e.g., LOINC codes).

    It requires authentication via a bearer token, which is verified by the `verify_token` dependency.

    :param patient_id: The ID of the patient whose observations should be retrieved.
    :param _: Parameter is used only to trigger token verification via dependency injection.
    :raises HTTPException:
        - 401 if token verification fails.
        - 404 if no observations are found for the given patient.
    :return: A dictionary containing:
        - patientId (str): The patient's ID.
        - observationCount (int): Total number of observations.
        - latest (dict): The latest observation data.
        - averageByCode (dict): Mapping of observation code to average value.
    """

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
