# MoMo SMS REST API Documentation

## Overview
This REST API provides secure access to Mobile Money (MoMo) SMS transaction records parsed from `modified_sms_v2.xml`. It supports full CRUD operations protected by HTTP Basic Authentication.

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
Basic Auth transmits credentials as a Base64-encoded string (not encrypted). Anyone intercepting the request can decode it instantly. It also has no token expiry, no revocation mechanism, and no scope control.

### Stronger Alternatives
| Method | Benefit |
|--------|---------|
| **JWT (JSON Web Tokens)** | Stateless, signed tokens with expiry. No credential re-transmission per request. |
| **OAuth 2.0** | Delegated authorization with scopes, refresh tokens, and third-party identity support. |
| **API Keys + HTTPS** | Simple key-based auth over TLS — better than Basic Auth but still lacks expiry/scopes. |

---

## Transaction Object Schema

```json
{
  "id": 1,
  "address": "+250788000000",
  "date": "1610000000000",
  "type": "1",
  "body": "You received 10,000 RWF from John Doe.",
  "amount": "10000",
  "sender": "John Doe",
  "receiver": "Peter Kamau"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique transaction identifier |
| `address` | string | Phone number associated with the SMS |
| `date` | string | Unix timestamp (milliseconds) |
| `type` | string | SMS type code |
| `body` | string | Raw SMS message body |
| `amount` | string | Transaction amount in RWF |
| `sender` | string | Name of the sender |
| `receiver` | string | Name of receiver |

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
curl.exe -u admin:secret123 http://localhost:8000/transactions
```

**Success Response — 200 OK:**
```json
[
  {
    "id": 1,
    "address": "+250788000000",
    "date": "1610000000000",
    "type": "1",
    "body": "You received 10,000 RWF from John Doe.",
    "amount": "10000",
    "sender": "John Doe",
    "receiver": "Peter Kamau"
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
curl.exe -u admin:secret123 http://localhost:8000/transactions/1
```

**Success Response — 200 OK:**
```json
{
  "id": 1,
  "address": "+250788000000",
  "date": "1610000000000",
  "type": "1",
  "body": "You received 10,000 RWF from John Doe.",
  "amount": "10000",
  "sender": "John Doe",
  "receiver": "Peter Kamau"
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
Create a new transaction record.

- **Method:** `POST`
- **URL:** `/transactions`
- **Auth Required:** Yes
- **Content-Type:** `application/json`

**Request Example:**
```powershell
$headers = @{ Authorization = "Basic " + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:secret123")) }
$body = '{"address":"+250788111222","amount":"5000","sender":"Alice","receiver":"Bob"}'
Invoke-RestMethod -Uri "http://localhost:8000/transactions" -Method POST -Headers $headers -ContentType "application/json" -Body $body
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
| 400 | Invalid or malformed JSON body |
| 401 | Missing or invalid credentials |

---

### 4. PUT /transactions/{id}
Update an existing transaction record by ID.

- **Method:** `PUT`
- **URL:** `/transactions/{id}`
- **Auth Required:** Yes
- **Content-Type:** `application/json`

**Request Example:**
```powershell
$body = '{"amount":"12000"}'
Invoke-RestMethod -Uri "http://localhost:8000/transactions/1" -Method PUT -Headers $headers -ContentType "application/json" -Body $body
```

**Request Body (partial update supported):**
```json
{
  "amount": "12000"
}
```

**Success Response — 200 OK:**
```json
{
  "id": 1,
  "address": "+250788000000",
  "date": "1610000000000",
  "type": "1",
  "body": "You received 10,000 RWF from John Doe.",
  "amount": "12000",
  "sender": "John Doe",
  "receiver": "Peter Kamau"
}
```

**Error Responses:**
| Code | Meaning |
|------|---------|
| 400 | ID not an integer, or invalid JSON body |
| 401 | Missing or invalid credentials |
| 404 | Transaction with given ID not found |

---

### 5. DELETE /transactions/{id}
Delete a transaction record by ID.

- **Method:** `DELETE`
- **URL:** `/transactions/{id}`
- **Auth Required:** Yes

**Request Example:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/transactions/1" -Method DELETE -Headers $headers
```

**Success Response — 200 OK:**
```json
{
  "message": "Transaction 1 deleted successfully"
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

All error responses follow this structure:

```json
{
  "error": "Not Found",
  "message": "Transaction not found"
}
```

| Field | Description |
|-------|-------------|
| `error` | Short HTTP status label |
| `message` | Human-readable explanation |

---

## HTTP Status Code Summary

| Code | Status | When It Occurs |
|------|--------|----------------|
| 200 | OK | Successful GET, PUT, DELETE |
| 201 | Created | Successful POST |
| 400 | Bad Request | Invalid ID format or malformed JSON |
| 401 | Unauthorized | Missing or wrong credentials |
| 404 | Not Found | Transaction ID does not exist or unknown endpoint |