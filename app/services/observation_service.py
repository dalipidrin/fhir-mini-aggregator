from fastapi import HTTPException
from ..models.observation import Observation


class ObservationService:
    """
    Service class responsible for operations related to Observation resources.

    Provides methods to validate the integrity and required fields of Observation objects to ensure they meet the expected criteria before
    further processing or storage.
    """

    @staticmethod
    def validate_observation(observation: Observation):
        """
        Validates the required fields of an Observation resource.

        Validations:
        - `resourceType` must be "Observation".
        - `subject.reference` must start with "Patient/".
        - `code.coding` list must not be empty and must include a `code`.
        - `valueQuantity.value` must be present.

        Raises HTTPException with status 400 if validation fails.

        :param observation: The Observation resource to validate.
        :raise HTTPException: If any required fields are missing or invalid.
        """
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
