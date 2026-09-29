#!/bin/bash

BASE_URL="http://localhost:8000"
VALID_AUTH="admin:secret123"
INVALID_AUTH="admin:wrongpass"
PASS=0
FAIL=0

check() {
    local description="$1"
    local expected="$2"
    local actual="$3"
    if echo "$actual" | grep -q "$expected"; then
        echo "  PASS: $description"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $description (expected '$expected' in response)"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== 1. No credentials (401) ==="
R=$(curl -i -s "$BASE_URL/transactions")
echo "$R" | head -1
check "No credentials returns 401" "401" "$R"

echo -e "\n=== 2. Wrong credentials (401) ==="
R=$(curl -i -s -u "$INVALID_AUTH" "$BASE_URL/transactions")
echo "$R" | head -1
check "Wrong credentials returns 401" "401" "$R"

echo -e "\n=== 3. GET all transactions (200) ==="
R=$(curl -i -s -u "$VALID_AUTH" "$BASE_URL/transactions")
echo "$R" | head -1
check "GET all returns 200" "200" "$R"

echo -e "\n=== 4. GET single transaction (200) ==="
R=$(curl -i -s -u "$VALID_AUTH" "$BASE_URL/transactions/1")
echo "$R" | head -1
check "GET single returns 200" "200" "$R"

echo -e "\n=== 5. GET non-existent transaction (404) ==="
R=$(curl -i -s -u "$VALID_AUTH" "$BASE_URL/transactions/999999")
echo "$R" | head -1
check "GET missing ID returns 404" "404" "$R"

echo -e "\n=== 6. GET invalid ID (400) ==="
R=$(curl -i -s -u "$VALID_AUTH" "$BASE_URL/transactions/abc")
echo "$R" | head -1
check "GET non-integer ID returns 400" "400" "$R"

echo -e "\n=== 7. POST new transaction (201) ==="
R=$(curl -i -s -u "$VALID_AUTH" -X POST "$BASE_URL/transactions" \
  -H "Content-Type: application/json" \
  -d '{"address":"+250788111222","amount":"5000","sender":"Alice","receiver":"Bob"}')
echo "$R" | head -1
check "POST returns 201" "201" "$R"
NEW_ID=$(echo "$R" | grep -o '"id":[0-9]*' | tail -1 | grep -o '[0-9]*')
echo "  Created ID: $NEW_ID"

echo -e "\n=== 8. POST empty body (400) ==="
R=$(curl -i -s -u "$VALID_AUTH" -X POST "$BASE_URL/transactions" \
  -H "Content-Type: application/json" \
  -d '{}')
echo "$R" | head -1
check "POST empty body returns 400" "400" "$R"

echo -e "\n=== 9. PUT update transaction (200) ==="
R=$(curl -i -s -u "$VALID_AUTH" -X PUT "$BASE_URL/transactions/$NEW_ID" \
  -H "Content-Type: application/json" \
  -d '{"amount":"9999"}')
echo "$R" | head -1
check "PUT returns 200" "200" "$R"

echo -e "\n=== 10. DELETE transaction (200) ==="
R=$(curl -i -s -u "$VALID_AUTH" -X DELETE "$BASE_URL/transactions/$NEW_ID")
echo "$R" | head -1
check "DELETE returns 200" "200" "$R"

echo -e "\n=== 11. DELETE already-deleted (404) ==="
R=$(curl -i -s -u "$VALID_AUTH" -X DELETE "$BASE_URL/transactions/$NEW_ID")
echo "$R" | head -1
check "DELETE missing ID returns 404" "404" "$R"

echo -e "\n================================"
echo "Results: $PASS passed, $FAIL failed"
