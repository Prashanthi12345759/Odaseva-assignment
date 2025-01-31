#!/bin/bash

# Test CreateCandidate
curl -X POST http://<function-app-url>/api/CreateCandidate -H "Content-Type: application/json" -d '{
  "specialty": "Informatique",
  "candidateId": "CA-000008",
  "candidateFirstName": "John",
  "candidateLastName": "Doe",
  "candidateBirthDate": "1980-01-01",
  "cv": "base64-encoded-pdf"
}'

# Test GetCandidate
curl -X GET http://<function-app-url>/api/GetCandidate/CA-000008

# Test GetCandidatesBySpecialty
curl -X GET http://<function-app-url>/api/GetCandidatesBySpecialty/Informatique