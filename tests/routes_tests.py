from fastapi.testclient import TestClient

from app.main import app
from app.models.observation import Observation
from app.routes.routes import observations_db

client = TestClient(app)


class TestFHIRAggregator:
    """
    Unit tests for the FHIR Mini Aggregator API.

    This test suite uses FastAPI's TestClient to simulate API calls for authentication, creating observations, and retrieving patient
    metrics. It verifies both successful flows and error handling.
    """

    def setup_method(self, method):
        # runs before each test method
        observations_db.clear()

    def add_test_observation(self):
        observation_dict = {
            "resourceType": "Observation",
            "id": "obs1",
            "status": "final",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "8462-4",
                        "display": "Diastolic blood pressure"
                    }
                ]
            },
            "subject": {
                "reference": "Patient/123"
            },
            "effectiveDateTime": "2025-01-10T10:00:00+02:00",
            "valueQuantity": {
                "value": 75,
                "unit": "mmHg"
            }
        }
        obs = Observation(**observation_dict)
        observations_db.append(obs)

    def get_auth_token(self):
        response = client.post(
            "/auth",
            data={"username": "user", "password": "pass"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        return response.json().get("access_token")

    def test_auth_that_ok(self):
        # given / when
        response = client.post(
            "/auth",
            data={"username": "user", "password": "pass"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        # then
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_create_observation_that_ok(self):
        # given
        token = self.get_auth_token()
        payload = [
            {
                "resourceType": "Patient",
                "id": "123",
                "name": [{"family": "Hardy", "given": ["Peter"]}],
                "birthDate": "1990-04-05"
            },
            {
                "resourceType": "Observation",
                "id": "obs2",
                "status": "final",
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "8462-4",
                            "display": "Diastolic blood pressure"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/123"
                },
                "effectiveDateTime": "2025-01-10T11:00:00+02:00",
                "valueQuantity": {
                    "value": 80,
                    "unit": "mmHg"
                }
            }
        ]

        # when
        response = client.post(
            "/observations",
            json=payload,
            headers={"Authorization": f"Bearer {token}"}
        )

        # then
        assert response.status_code in (200, 201)

    def test_create_observation_with_invalid_bearer_token_that_401(self):
        # given
        payload = [
            {
                "resourceType": "Patient",
                "id": "123",
                "name": [{"family": "Hardy", "given": ["Peter"]}],
                "birthDate": "1990-04-05"
            },
            {
                "resourceType": "Observation",
                "id": "obs2",
                "status": "final",
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "8462-4",
                            "display": "Diastolic blood pressure"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/123"
                },
                "effectiveDateTime": "2025-01-10T11:00:00+02:00",
                "valueQuantity": {
                    "value": 80,
                    "unit": "mmHg"
                }
            }
        ]

        # when
        response = client.post(
            "/observations",
            json=payload,
            headers={"Authorization": "Bearer invalid token"}
        )

        # then
        assert response.status_code == 401

    def test_get_patient_metrics_that_ok(self):
        # given
        token = self.get_auth_token()
        self.add_test_observation()

        # when
        response = client.get(
            "/patients/123/metrics",
            headers={"Authorization": f"Bearer {token}"}
        )

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["patientId"] == "123"
        assert data["observationCount"] == 1
        assert "latest" in data
        assert "averageByCode" in data
        assert data["averageByCode"]["8462-4"] == 75

    def test_get_patient_metrics_with_invalid_bearer_token_that_401(self):
        # given
        self.add_test_observation()

        # when
        response = client.get(
            "/patients/123/metrics",
            headers={"Authorization": "Bearer invalid token"}
        )

        # then
        assert response.status_code == 401

    def test_get_patient_metrics_with_no_observations_that_404(self):
        # given
        token = self.get_auth_token()

        # when
        response = client.get(
            "/patients/999/metrics",
            headers={"Authorization": f"Bearer {token}"}
        )

        # then
        assert response.status_code == 404
