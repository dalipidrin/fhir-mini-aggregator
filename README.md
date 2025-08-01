# FHIR Mini Aggregator

FHIR Mini Aggregator that ingests raw clinical data (FHIR/HL7) and turns it into actionable insights.

---

## Setup

1. **Clone the repo**

```bash
git clone <repo_url>
cd fhir-mini-aggregator
```

2. **Run the project**
```bash
uvicorn app.main:app
```

## Endpoints

1. **Authorization**

Request:
```bash
curl -X POST "http://127.0.0.1:8000/auth" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user&password=pass"
```
Response:
```bash
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

2. **Observations**

Request:
```bash
curl -X POST "http://127.0.0.1:8000/observations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <jwt_token>" \
  -d '[
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
              {"system": "http://loinc.org", "code": "8462-4", "display": "Diastolic blood pressure"}
            ]
          },
          "subject": {"reference": "Patient/123"},
          "effectiveDateTime": "2025-01-10T10:00:00+02:00",
          "valueQuantity": {"value": 100, "unit": "mmHg"}
        }
      ]'
```
Response:
```bash
{
  "message": "Observation stored successfully",
  "id": "obs1"
}
```

3. **Patient metrics**

Request:
```bash
curl -X GET "http://127.0.0.1:8000/patients/123/metrics" \
  -H "Authorization: Bearer <your_jwt_token>"
```
Response:
```bash
{
  "patientId": "123",
  "observationCount": 1,
  "latest": {
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
  },
  "averageByCode": {
    "8462-4": 75
  }
}
```

## Docker

To spin up the API quickly using Docker Compose, run:

```bash
docker-compose up --build
```

## Reasoning

### Security
All protected endpoints require a JWT Bearer token issued via `/auth`. This keeps the API secure without adding complex user management.

### Minimal, relevant model validation
Validates key FHIR Observation fields to keep logic clear and simple, focusing on required identifiers and codes.

### In-memory storage
Uses an in-memory list (`observations_db`) for simplicity.

### Extensible foundation
Built with FastAPI and Pydantic for strong typing, validation, and rapid API development.
