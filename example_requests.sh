#!/usr/bin/env bash
curl -X 'PUT' \
  'http://localhost:8000/log/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "customer_id": "cac22779-bbf7-442b-a609-736d2429d0b2",
  "description": "The new account is created",
  "event_timestamp": "2024-01-04T00:00:00",
  "event_type": "CREATE_ACCOUNT",
  "service_id": "550e8400-e29b-41d4-a716-446655440003"
}'


resp="$(curl -X 'GET' \
  'http://localhost:8000/log/?limit=10' \
  -H 'accept: application/json')"

echo $resp

curl -X 'PUT' \
  'http://localhost:8000/log/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "customer_id": "cac22779-bbf7-442b-a609-736d2429d0b2",
  "description": "The new account is created",
  "event_timestamp": "2024-02-04T00:00:00",
  "event_type": "DELETE_ACCOUNT",
  "service_id": "550e8400-e29b-41d4-a716-446655440003"
}'

resp="$(curl -X 'GET' \
  'http://localhost:8000/log/?limit=10&event_type=DELETE_ACCOUNT' \
  -H 'accept: application/json')"

echo $resp

resp="$(curl -X 'GET' \
  'http://localhost:8000/log/?limit=10&event_type=DELETE_ACCOUNT&last_seen_datetime=2024-01-22T08:47:36.869Z' \
  -H 'accept: application/json')"

echo $resp