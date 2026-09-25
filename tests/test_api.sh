#!/bin/bash

BASE_URL="http://localhost:8000"
VALID_AUTH="admin:secret123"
INVALID_AUTH="admin:wrongpass"

echo "=== 1. Test Unauthorized Access (401) ==="
curl -i -s "$BASE_URL/transactions"

echo -e "\n=== 2. Test Invalid Credentials (401) ==="
curl -i -s -u "$INVALID_AUTH" "$BASE_URL/transactions"

echo -e "\n=== 3. Test GET All Transactions (200) ==="
curl -i -s -u "$VALID_AUTH" "$BASE_URL/transactions"

echo -e "\n=== 4. Test GET Single Transaction (200) ==="
curl -i -s -u "$VALID_AUTH" "$BASE_URL/transactions/1"

echo -e "\n=== 5. Test POST New Transaction (201) ==="
curl -i -s -u "$VALID_AUTH" -X POST "$BASE_URL/transactions" \
  -H "Content-Type: application/json" \
  -d '{"address":"+250788111222","amount":"5000","sender":"Alice","receiver":"Bob"}'

echo -e "\n=== 6. Test PUT Update Transaction (200) ==="
curl -i -s -u "$VALID_AUTH" -X PUT "$BASE_URL/transactions/1" \
  -H "Content-Type: application/json" \
  -d '{"amount":"12000"}'

echo -e "\n=== 7. Test DELETE Transaction (200) ==="
curl -i -s -u "$VALID_AUTH" -X DELETE "$BASE_URL/transactions/1"
