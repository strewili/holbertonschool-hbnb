# HBnB Part 2 — Testing Report

**Project:** HBnB Evolution — Part 2 (Business Logic and API Endpoints)
**Team:** Alhazmi Jana, Shouq Alqarni, Kayan Alnazari
**Scope:** Task 5 (Review Endpoints) and Task 6 (Testing and Validation)

---

## 1. Environment

- Server started with: `python3 -m app.run`
- Base URL: `http://127.0.0.1:5000`
- Swagger documentation available at: `http://127.0.0.1:5000/api/v1/`
- Namespaces registered and confirmed visible in Swagger: `users`, `amenities`, `places`, `reviews`

---

## 2. Setup Data Used for Testing

| Entity | ID | Notes |
|---|---|---|
| User | `60bffba8-d637-4839-91e0-c18f86d5f58e` | Kayan Alnazari, kayan@test.com |
| Place | `db01c87b-946d-4ed5-8269-ac296f3226f0` | "Nice Apartment", owned by user above |
| Review | `aa4d4507-3e13-4fd8-9e50-0f80fd9eb6d6` | Created, updated, then deleted during testing |

---

## 3. Task 5 — Review Endpoint Tests (CRUD)

### 3.1 POST /api/v1/reviews/ — Create Review

**Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Great place", "rating": 5, "user_id": "60bffba8-d637-4839-91e0-c18f86d5f58e", "place_id": "db01c87b-946d-4ed5-8269-ac296f3226f0"}'
```

**Result:** `201 Created`
```json
{
    "id": "aa4d4507-3e13-4fd8-9e50-0f80fd9eb6d6",
    "text": "Great place",
    "rating": 5,
    "user_id": "60bffba8-d637-4839-91e0-c18f86d5f58e",
    "place_id": "db01c87b-946d-4ed5-8269-ac296f3226f0"
}
```
**Status:** ✅ PASS

---

### 3.2 GET /api/v1/reviews/{id} — Retrieve Review

**Request:**
```bash
curl http://127.0.0.1:5000/api/v1/reviews/aa4d4507-3e13-4fd8-9e50-0f80fd9eb6d6
```

**Result:** `200 OK`
```json
{
    "id": "aa4d4507-3e13-4fd8-9e50-0f80fd9eb6d6",
    "text": "Great place",
    "rating": 5,
    "user_id": "60bffba8-d637-4839-91e0-c18f86d5f58e",
    "place_id": "db01c87b-946d-4ed5-8269-ac296f3226f0"
}
```
**Status:** ✅ PASS

---

### 3.3 PUT /api/v1/reviews/{id} — Update Review

**Request:**
```bash
curl -X PUT http://127.0.0.1:5000/api/v1/reviews/aa4d4507-3e13-4fd8-9e50-0f80fd9eb6d6 \
  -H "Content-Type: application/json" \
  -d '{"text": "Amazing place, updated!", "rating": 4, "user_id": "60bffba8-d637-4839-91e0-c18f86d5f58e", "place_id": "db01c87b-946d-4ed5-8269-ac296f3226f0"}'
```

**Result:** `200 OK`
```json
{
    "id": "aa4d4507-3e13-4fd8-9e50-0f80fd9eb6d6",
    "text": "Amazing place, updated!",
    "rating": 4,
    "user_id": "60bffba8-d637-4839-91e0-c18f86d5f58e",
    "place_id": "db01c87b-946d-4ed5-8269-ac296f3226f0"
}
```
**Status:** ✅ PASS — fields correctly reflected the update.

---

### 3.4 DELETE /api/v1/reviews/{id} — Delete Review

**Request:**
```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/aa4d4507-3e13-4fd8-9e50-0f80fd9eb6d6
```

**Result:** `200 OK`
```json
{
    "message": "Review deleted successfully"
}
```
**Status:** ✅ PASS

**Verification — GET after DELETE:**
```bash
curl http://127.0.0.1:5000/api/v1/reviews/aa4d4507-3e13-4fd8-9e50-0f80fd9eb6d6
```
**Result:** `404 Not Found`
```json
{
    "error": "Review not found"
}
```
**Status:** ✅ PASS — review correctly no longer retrievable after deletion.

---

## 4. Task 6 — Validation and Edge Case Tests

### 4.1 Invalid rating (out of 1–5 range)

**Request:**
```bash
curl -i -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Bad rating test", "rating": 10, "user_id": "60bffba8-d637-4839-91e0-c18f86d5f58e", "place_id": "db01c87b-946d-4ed5-8269-ac296f3226f0"}'
```

**Result:** `400 BAD REQUEST`
```json
{
    "error": "rating must be an integer between 1 and 5"
}
```
**Status:** ✅ PASS — rejected as expected, no crash.

---

### 4.2 Empty review text

**Request:**
```bash
curl -i -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{"text": "", "rating": 4, "user_id": "60bffba8-d637-4839-91e0-c18f86d5f58e", "place_id": "db01c87b-946d-4ed5-8269-ac296f3226f0"}'
```

**Result:** `400 BAD REQUEST`
```json
{
    "error": "text is required and must be a string"
}
```
**Status:** ✅ PASS

---

### 4.3 Nonexistent user_id

**Request:**
```bash
curl -i -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{"text": "test review", "rating": 3, "user_id": "fake-id-999", "place_id": "db01c87b-946d-4ed5-8269-ac296f3226f0"}'
```

**Result:** `400 BAD REQUEST`
```json
{
    "error": "User or Place not found"
}
```
**Status:** ✅ PASS — foreign key relationship correctly validated before creating the review.

---

## 5. Summary Table

| # | Test | Endpoint | Expected | Actual | Result |
|---|---|---|---|---|---|
| 1 | Create valid review | POST /reviews/ | 201 | 201 | ✅ PASS |
| 2 | Get review by id | GET /reviews/{id} | 200 | 200 | ✅ PASS |
| 3 | Update review | PUT /reviews/{id} | 200 | 200 | ✅ PASS |
| 4 | Delete review | DELETE /reviews/{id} | 200 | 200 | ✅ PASS |
| 5 | Get deleted review | GET /reviews/{id} | 404 | 404 | ✅ PASS |
| 6 | Rating out of range | POST /reviews/ | 400 | 400 | ✅ PASS |
| 7 | Empty text | POST /reviews/ | 400 | 400 | ✅ PASS |
| 8 | Nonexistent user_id | POST /reviews/ | 400 | 400 | ✅ PASS |

**Total: 8/8 tests passed.**

---

## 6. Issues Found and Resolved During Development

1. **IndentationError in `facade.py`** — the `get_review` method definition and its body were incorrectly indented (mixed spacing), causing the app to fail on startup. Fixed by correcting indentation to standard 4-space blocks.
2. **Circular import in `app/persistence/__init__.py`** — this file incorrectly contained a duplicate copy of the `create_app()` factory function (which belongs in `app/__init__.py`), including an import from `app.api.v1.users`. Since the persistence layer must not depend on the API layer, this caused a circular import. Fixed by clearing `persistence/__init__.py` down to a simple package docstring.

---

## 7. Conclusion

All CRUD operations for the Review entity function as expected, and validation logic correctly rejects invalid input (bad rating range, empty text, nonexistent related entities) with appropriate `400` status codes rather than failing silently or crashing. The Facade correctly mediates between the Presentation (API) and Business Logic layers. Swagger documentation at `/api/v1/` accurately reflects all four namespaces (`users`, `amenities`, `places`, `reviews`).

