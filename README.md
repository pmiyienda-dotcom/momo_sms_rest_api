# Building and Securing a MoMo REST API & DSA Performance Benchmarking

A lightweight Python-based RESTful API service that parses Mobile Money (MoMo) XML transaction logs, exposes full CRUD operations with HTTP Basic Authentication, and benchmarks lookup algorithms (O(N) Linear Search and O(1) Dictionary Lookup) across 1,600+ parsed records.

---

## Project Overview

1. **XML Data Pipeline**: Parses `modified_sms_v2.xml` into structured JSON records stored in `api/mock_db.json`.
2. **RESTful API Service**: Full CRUD endpoints using Python's native `http.server`.
3. **Authentication & Security**: All endpoints protected with HTTP Basic Authentication.
4. **DSA Benchmarking**: Compares Linear Search O(N) vs Dictionary Lookup O(1) on real transaction data.

---

## Repository Structure

```text
├── api/
│   ├── auth.py              # Basic Authentication validation logic
│   ├── server.py            # REST API server (GET, POST, PUT, DELETE)
│   └── mock_db.json         # Parsed JSON transaction database
├── dsa/
│   ├── parse_xml.py         # XML → JSON parser
│   └── benchmark.py         # DSA benchmark: Linear Search vs Dictionary Lookup
├── docs/
│   └── api_docs.md          # Full API endpoint documentation
├── screenshots/
│   ├── All transactions.png
│   ├── Creating New Transaction.png
│   ├── Deleting transactions.png
│   ├── GET All Transactions.png
│   ├── Single Transaction.png
│   └── Updating Existing Transaction.png
├── tests/
│   └── test_api.sh          # curl-based API test script
├── hashmap.py               # Standalone DSA demo: Linear Search vs Dictionary Lookup
├── modified_sms_v2.xml      # Raw Mobile Money XML dataset
├── benchmark_results.txt    # Saved benchmark output
└── README.md
```

---

## Setup & Execution

### Prerequisites
- Python 3.8+
- PowerShell or Terminal

### 1. Parse the XML Dataset

```powershell
python dsa/parse_xml.py
```

Outputs parsed records to `api/mock_db.json`.

### 2. Run the REST API Server

```powershell
python api/server.py
```

Server starts at `http://localhost:8000`.

### 3. Run DSA Benchmark

```powershell
python dsa/benchmark.py
```

Results are printed to console and saved to `benchmark_results.txt`.

---

## API Endpoints

All endpoints require HTTP Basic Authentication:
- **Username:** `admin`
- **Password:** `secret123`

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| GET | `/transactions` | Retrieve all transactions | 200 OK |
| GET | `/transactions/{id}` | Retrieve one transaction | 200 / 404 |
| POST | `/transactions` | Add a new transaction | 201 / 400 |
| PUT | `/transactions/{id}` | Update a transaction | 200 / 404 |
| DELETE | `/transactions/{id}` | Delete a transaction | 200 / 404 |

---

## Testing the API

### Unauthorized Request (401)
```powershell
curl.exe -u wronguser:wrongpass http://localhost:8000/transactions
```

### GET All Transactions
```powershell
curl.exe -u admin:secret123 http://localhost:8000/transactions
```

### POST — Create New Transaction
```powershell
$headers = @{ Authorization = "Basic " + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:secret123")) }
$body = '{"address":"+250788111222","amount":"5000","sender":"Alice","receiver":"Bob"}'
Invoke-RestMethod -Uri "http://localhost:8000/transactions" -Method POST -Headers $headers -ContentType "application/json" -Body $body
```

### PUT — Update Transaction
```powershell
$body = '{"amount":"12000"}'
Invoke-RestMethod -Uri "http://localhost:8000/transactions/1" -Method PUT -Headers $headers -ContentType "application/json" -Body $body
```

### DELETE — Remove Transaction
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/transactions/1" -Method DELETE -Headers $headers
```

---

## DSA Benchmark & Complexity Analysis

| Algorithm | Time Complexity | Space Complexity | Description |
|-----------|----------------|------------------|-------------|
| Linear Search | O(N) | O(1) | Scans records sequentially. Slower as N grows. |
| Dictionary Lookup | O(1) avg | O(N) | Direct key-value access via Python dict hash map. |

**Why is dictionary lookup faster?**
A Python dictionary uses a hash table internally. When you look up a key, Python computes its hash and jumps directly to the memory bucket — no scanning required. Linear search must check every element one by one, so time grows linearly with dataset size.

**Alternative data structure:** A **Binary Search Tree (BST)** or **sorted array with binary search** offers O(log N) lookup with lower memory overhead than a hash map, making it a good middle ground when memory is constrained and keys are ordered.
