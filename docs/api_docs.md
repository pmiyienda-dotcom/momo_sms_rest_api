# MoMo SMS REST API Documentation

## Overview
This REST API provides access to Mobile Money (MoMo) SMS transaction records parsed from `modified_sms_v2.xml` (1,691 records). It supports full CRUD operations protected by HTTP Basic Authentication. The persistence layer is a local JSON file (`api/mock_db.json`), not a database.

---

## Base URL
```
http://localhost:8000
```

---

## Authentication

All endpoints require HTTP Basic Authentication.

- **Scheme:** `Authorization: Basic <base64(username:password)>`
- **Credentials:** `admin:secret123`
- **Encoded header value:** `Basic YWRtaW46c2VjcmV0MTIz`

Requests with missing or invalid credentials return `401 Unauthorized`.

### Why Basic Auth is Weak
Basic Auth transmits credentials as a Base64-encoded string — not encrypted. Anyone intercepting the request over plain HTTP can decode it instantly. It also has no token expiry, no revocation mechanism, and no scope control.

### Stronger Alternatives
| Method | Benefit |
|--------|---------|
| **JWT (JSON Web Tokens)** | Stateless signed tokens with expiry. Credentials are not re-sent per request. |
| **OAuth 2.0** | Delegated authorization with scopes, refresh tokens, and third-party identity support. |
| **API Keys + HTTPS** | Simple key-based auth over TLS — better than Basic Auth but still lacks expiry and scopes. |

---

## Transaction Object Schema

Fields are derived by regex from raw SMS body text. 330 of 1,691 records (19.5%) match no pattern (mostly bank-deposit messages) and retain default values of `"0.0"` for amount and `"Unknown"` for sender/receiver.

```json
{
  "id": 1,
  "address": "M-Money",
  "date": "1609459200000",
  "type": "1",
  "body": "You have received 2,000 RWF from Jane Smith (250788000001) on your Mobile Money account at 2021-01-01 00:00:00.",
  "amount": "2000",
  "sender": "Jane Smith",
  "receiver": "Account Holder"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique transaction identifier (auto-assigned) |
| `address` | string | SMS sender address (e.g. `M-Money`) |
| `date` | string | Unix timestamp in milliseconds |
| `type` | string | SMS type code (`"1"` = received) |
| `body` | string | Raw SMS message body |
| `amount` | string | Transaction amount in RWF (`"0.0"` if unmatched) |
| `sender` | string | Parsed sender name (`"Unknown"` if unmatched) |
| `receiver` | string | Parsed receiver name (`"Unknown"` if unmatched) |

---

## Endpoints

---

### 1. GET /transactions
Retrieve all transaction records.

- **Method:** `GET`
- **URL:** `/transactions`
- **Auth Required:** Yes

**Request Example:**
```bash
curl.exe -i -u admin:secret123 http://localhost:8000/transactions
```

**Success Response — 200 OK:**
```json
[
  {
    "id": 1,
    "address": "M-Money",
    "date": "1609459200000",
    "type": "1",
    "body": "You have received 2,000 RWF from Jane Smith...",
    "amount": "2000",
    "sender": "Jane Smith",
    "receiver": "Account Holder"
  }
]
```

**Error Responses:**
| Code | Meaning |
|------|---------|
| 401 | Missing or invalid credentials |

---

### 2. GET /transactions/{id}
Retrieve a single transaction by its ID.

- **Method:** `GET`
- **URL:** `/transactions/{id}`
- **Auth Required:** Yes

**Request Example:**
```bash
curl.exe -i -u admin:secret123 http://localhost:8000/transactions/1
```

**Success Response — 200 OK:**
```json
{
  "id": 1,
  "address": "M-Money",
  "date": "1609459200000",
  "type": "1",
  "body": "You have received 2,000 RWF from Jane Smith...",
  "amount": "2000",
  "sender": "Jane Smith",
  "receiver": "Account Holder"
}
```

**Error Responses:**
| Code | Meaning |
|------|---------|
| 400 | ID is not a valid integer |
| 401 | Missing or invalid credentials |
| 404 | Transaction with given ID not found |

---

### 3. POST /transactions
Create a new transaction record. The body must be a non-empty JSON object.

- **Method:** `POST`
- **URL:** `/transactions`
- **Auth Required:** Yes
- **Content-Type:** `application/json`

**Request Example:**
```bash
curl.exe -i -u admin:secret123 -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d "{\"address\":\"+250788111222\",\"amount\":\"5000\",\"sender\":\"Alice\",\"receiver\":\"Bob\"}"
```

**Request Body:**
```json
{
  "address": "+250788111222",
  "amount": "5000",
  "sender": "Alice",
  "receiver": "Bob"
}
```

**Success Response — 201 Created:**
```json
{
  "id": 1692,
  "address": "+250788111222",
  "amount": "5000",
  "sender": "Alice",
  "receiver": "Bob"
}
```

**Error Responses:**
| Code | Meaning |
|------|---------|
| 400 | Malformed JSON, non-object body (e.g. array), or empty body |
| 401 | Missing or invalid credentials |

---

### 4. PUT /transactions/{id}
Partially update an existing transaction. Only the fields supplied in the body are changed — omitted fields keep their current values.

- **Method:** `PUT`
- **URL:** `/transactions/{id}`
- **Auth Required:** Yes
- **Content-Type:** `application/json`

**Request Example:**
```bash
curl.exe -i -u admin:secret123 -X PUT http://localhost:8000/transactions/2 \
  -H "Content-Type: application/json" \
  -d "{\"amount\":\"12000\"}"
```

**Request Body (partial update):**
```json
{
  "amount": "12000"
}
```

**Success Response — 200 OK:**
```json
{
  "id": 2,
  "address": "M-Money",
  "date": "1609459200000",
  "type": "1",
  "body": "...",
  "amount": "12000",
  "sender": "Account Holder",
  "receiver": "Account Holder"
}
```

**Known Limitation:** PUT behaves as a partial update (`record.update()`). It does not replace the full record. Supplying a non-object body (e.g. an array) returns 400.

**Error Responses:**
| Code | Meaning |
|------|---------|
| 400 | ID not an integer, malformed JSON, or non-object body |
| 401 | Missing or invalid credentials |
| 404 | Transaction with given ID not found |

---

### 5. DELETE /transactions/{id}
Delete a transaction record by ID.

- **Method:** `DELETE`
- **URL:** `/transactions/{id}`
- **Auth Required:** Yes

**Request Example:**
```bash
curl.exe -i -u admin:secret123 -X DELETE http://localhost:8000/transactions/2
```

**Success Response — 200 OK:**
```json
{
  "message": "Transaction 2 deleted successfully"
}
```

**Error Responses:**
| Code | Meaning |
|------|---------|
| 400 | ID is not a valid integer |
| 401 | Missing or invalid credentials |
| 404 | Transaction with given ID not found |

---

## Error Response Format

All error responses use this structure:

```json
{
  "error": "Bad Request",
  "message": "ID must be an integer"
}
```

| Field | Description |
|-------|-------------|
| `error` | Short HTTP status label |
| `message` | Human-readable explanation of the specific problem |

---

## HTTP Status Code Summary

| Code | Status | When It Occurs |
|------|--------|----------------|
| 200 | OK | Successful GET, PUT, DELETE |
| 201 | Created | Successful POST |
| 400 | Bad Request | Non-integer ID, malformed JSON, empty or non-object body |
| 401 | Unauthorized | Missing or wrong credentials |
| 404 | Not Found | Transaction ID does not exist or unknown endpoint |
