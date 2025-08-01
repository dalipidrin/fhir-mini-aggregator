from fastapi import HTTPException

from ..models.observation import Observation


class PatientService:
    """
    Service class responsible for operations related to Patient resources.

    Provides methods to get observations for a specific patient and calculate average value of observations grouped by their observation
    code.
    """

    @staticmethod
    def get_observations_for_patient(patient_id: str, observations: list[Observation]) -> list[Observation]:
        """
        Filters the list of observations to those that belong to the specified patient.

        :param patient_id: The ID of the patient to filter observations for.
        :param observations: List of Observation objects to filter.
        :raise HTTPException: Raises 404 if no observations are found for the given patient.
        :return: List of Observation objects for the patient.
        """
        filtered_observations = [obs for obs in observations if obs.subject.reference == f"Patient/{patient_id}"]
        if not filtered_observations:
            raise HTTPException(status_code=404, detail="No observations found for this patient")
        return filtered_observations

    @staticmethod
    def calculate_average_by_code(patient_observations: list[Observation]) -> dict:
        """
        Calculates the average value of observations grouped by their observation code.

        Iterates over a list of Observation objects, sums the `valueQuantity.value` for each unique observation code (e.g., LOINC code),
        counts the occurrences, and computes the average per code.

        :param patient_observations: List of Observation objects to process.
        :return: A dictionary mapping observation codes (str) to their average value (float).
        """
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

        return average_by_code
