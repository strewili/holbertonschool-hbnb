# HBnB Part 2 — Testing Report

**Project:** HBnB Evolution — Part 2 (Business Logic and API Endpoints)
**Team:** Alhazmi Jana, Shouq Alqarni, Kayan Alnazari
**Scope:** Task 5 (Review Endpoints) and Task 6 (Testing and Validation — all entities)

---

## 1. Environment

- Server started with: `python3 -m app.run`
- Base URL: `http://127.0.0.1:5000`
- Swagger documentation available at: `http://127.0.0.1:5000/api/v1/`
- Namespaces registered and confirmed visible in Swagger: `users`, `amenities`, `places`, `reviews`

---

## 2. Users — Endpoint Tests

### 2.1 POST /api/v1/users/ — Create User
**Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Kayan", "last_name": "Alnazari", "email": "kayan3@test.com"}'
```
**Result:** `201 Created`
```json
{
    "id": "f8d5aa63-89e1-49c3-93cb-ff13d235af13",
    "first_name": "Kayan",
    "last_name": "Alnazari",
    "email": "kayan3@test.com"
}
```
**Status:** ✅ PASS

### 2.2 GET /api/v1/users/{id} — Retrieve User
**Result:** `200 OK` — returned the user created above.
**Status:** ✅ PASS

### 2.3 GET /api/v1/users/ — List All Users
**Result:** `200 OK` — returned array containing the created user.
**Status:** ✅ PASS

### 2.4 PUT /api/v1/users/{id} — Update User
**Request:**
```bash
curl -X PUT http://127.0.0.1:5000/api/v1/users/f8d5aa63-89e1-49c3-93cb-ff13d235af13 \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Kayan", "last_name": "Alnazari Updated", "email": "kayan3@test.com"}'
```
**Result:** `200 OK`
```json
{
    "id": "f8d5aa63-89e1-49c3-93cb-ff13d235af13",
    "first_name": "Kayan",
    "last_name": "Alnazari Updated",
    "email": "kayan3@test.com"
}
```
**Status:** ✅ PASS (after bug fix — see Section 6)

### 2.5 Validation — Duplicate email
**Request:** POST with an email already registered.
**Result:** `400`
```json
{"error": "Email already registered"}
```
**Status:** ✅ PASS — duplicate email correctly rejected.

---

## 3. Places — Endpoint Tests

### 3.1 POST /api/v1/places/ — Create Place
**Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Nice Apartment", "description": "test", "price": 100, "latitude": 24.7, "longitude": 46.6, "owner_id": "f8d5aa63-89e1-49c3-93cb-ff13d235af13", "amenities": []}'
```
**Result:** `201 Created`
```json
{
    "id": "80f068ed-4c87-48e8-86ec-773eac40107b",
    "title": "Nice Apartment",
    "description": "test",
    "price": 100.0,
    "latitude": 24.7,
    "longitude": 46.6,
    "owner_id": "f8d5aa63-89e1-49c3-93cb-ff13d235af13"
}
```
**Status:** ✅ PASS
**Note:** `amenities` is a required field in the payload (even if empty `[]`).

### 3.2 GET /api/v1/places/{id} — Retrieve Place (extended attributes)
**Result:** `200 OK`
```json
{
    "id": "80f068ed-4c87-48e8-86ec-773eac40107b",
    "title": "Nice Apartment",
    "description": "test",
    "price": 100.0,
    "latitude": 24.7,
    "longitude": 46.6,
    "owner": {
        "id": "f8d5aa63-89e1-49c3-93cb-ff13d235af13",
        "first_name": "Kayan",
        "last_name": "Alnazari Updated",
        "email": "kayan3@test.com"
    },
    "amenities": []
}
```
**Status:** ✅ PASS — response correctly includes full owner details (`first_name`, `last_name`, `email`) and amenities list, matching the project's serialization requirement.

### 3.3 GET /api/v1/places/ — List All Places
**Result:** `200 OK`
```json
[
    {
        "id": "80f068ed-4c87-48e8-86ec-773eac40107b",
        "title": "Nice Apartment",
        "latitude": 24.7,
        "longitude": 46.6
    }
]
```
**Status:** ✅ PASS

### 3.4 PUT /api/v1/places/{id} — Update Place
**Request:**
```bash
curl -X PUT http://127.0.0.1:5000/api/v1/places/80f068ed-4c87-48e8-86ec-773eac40107b \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Apartment", "description": "updated test", "price": 150, "latitude": 24.7, "longitude": 46.6, "owner_id": "f8d5aa63-89e1-49c3-93cb-ff13d235af13", "amenities": []}'
```
**Result:** `200 OK`
```json
{"message": "Place updated successfully"}
```
**Status:** ✅ PASS

---

## 4. Amenities — Endpoint Tests

### 4.1 POST /api/v1/amenities/ — Create Amenity
**Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'
```
**Result:** `201 Created`
```json
{"id": "395a640d-4b32-43e0-9346-d777d9243567", "name": "Wi-Fi"}
```
**Status:** ✅ PASS

### 4.2 GET /api/v1/amenities/ — List All Amenities
**Result:** `200 OK` — returned array with the created amenity.
**Status:** ✅ PASS

### 4.3 GET /api/v1/amenities/{id} — Retrieve Amenity
**Result:** `200 OK` — returned the amenity's `id` and `name`.
**Status:** ✅ PASS

### 4.4 PUT /api/v1/amenities/{id} — Update Amenity
**Request:**
```bash
curl -X PUT http://127.0.0.1:5000/api/v1/amenities/395a640d-4b32-43e0-9346-d777d9243567 \
  -H "Content-Type: application/json" \
  -d '{"name": "Free Wi-Fi"}'
```
**Result:** `200 OK`
```json
{"id": "395a640d-4b32-43e0-9346-d777d9243567", "name": "Free Wi-Fi"}
```
**Status:** ✅ PASS

---

## 5. Reviews — Endpoint Tests (Task 5 core requirement)

### 5.1 POST /api/v1/reviews/ — Create Review
**Result:** `201 Created` — review created and correctly linked to user and place.
**Status:** ✅ PASS

### 5.2 GET /api/v1/reviews/{id} — Retrieve Review
**Result:** `200 OK` — returned full review data.
**Status:** ✅ PASS

### 5.3 PUT /api/v1/reviews/{id} — Update Review
**Result:** `200 OK` — updated fields correctly reflected (`text`, `rating`).
**Status:** ✅ PASS

### 5.4 DELETE /api/v1/reviews/{id} — Delete Review
**Result:** `200 OK` — `{"message": "Review deleted successfully"}`
**Status:** ✅ PASS

### 5.5 GET after DELETE — Confirm Deletion
**Result:** `404 Not Found` — `{"error": "Review not found"}`
**Status:** ✅ PASS

### 5.6 Validation — Rating out of range (>5)
**Result:** `400 BAD REQUEST` — `{"error": "rating must be an integer between 1 and 5"}`
**Status:** ✅ PASS

### 5.7 Validation — Empty review text
**Result:** `400 BAD REQUEST` — `{"error": "text is required and must be a string"}`
**Status:** ✅ PASS

### 5.8 Validation — Nonexistent user_id
**Result:** `400 BAD REQUEST` — `{"error": "User or Place not found"}`
**Status:** ✅ PASS

---

## 6. Issues Found and Resolved During Development

1. **IndentationError in `facade.py` (`get_review`)** — the method definition and body had inconsistent indentation, crashing the app at import time. Fixed by correcting indentation to standard 4-space blocks.

2. **Circular import in `app/persistence/__init__.py`** — this file incorrectly contained a duplicate `create_app()` factory (which belongs in `app/__init__.py`), including an import from `app.api.v1.users`. Since the persistence layer must not depend on the API layer, this caused a circular import. Fixed by clearing `persistence/__init__.py` down to a simple package docstring.

3. **`update_user` returned `None` (`AttributeError: 'NoneType' object has no attribute 'id'`)** — the original implementation was:
   ```python
   def update_user(self, user_id, data):
       return self.user_repo.update(user_id, data)
   ```
   `repository.update()` does not return the updated object, so the endpoint crashed trying to read `.id` off `None`. Fixed to fetch and return the updated object explicitly:
   ```python
   def update_user(self, user_id, data):
       user = self.user_repo.get(user_id)
       if not user:
           return None
       self.user_repo.update(user_id, data)
       return self.user_repo.get(user_id)
   ```

---

## 7. Summary Table

| # | Entity | Test | Endpoint | Expected | Actual | Result |
|---|---|---|---|---|---|---|
| 1 | User | Create | POST /users/ | 201 | 201 | ✅ |
| 2 | User | Get by id | GET /users/{id} | 200 | 200 | ✅ |
| 3 | User | List all | GET /users/ | 200 | 200 | ✅ |
| 4 | User | Update | PUT /users/{id} | 200 | 200 | ✅ |
| 5 | User | Duplicate email rejected | POST /users/ | 400 | 400 | ✅ |
| 6 | Place | Create | POST /places/ | 201 | 201 | ✅ |
| 7 | Place | Get by id (extended attrs) | GET /places/{id} | 200 | 200 | ✅ |
| 8 | Place | List all | GET /places/ | 200 | 200 | ✅ |
| 9 | Place | Update | PUT /places/{id} | 200 | 200 | ✅ |
| 10 | Amenity | Create | POST /amenities/ | 201 | 201 | ✅ |
| 11 | Amenity | List all | GET /amenities/ | 200 | 200 | ✅ |
| 12 | Amenity | Get by id | GET /amenities/{id} | 200 | 200 | ✅ |
| 13 | Amenity | Update | PUT /amenities/{id} | 200 | 200 | ✅ |
| 14 | Review | Create | POST /reviews/ | 201 | 201 | ✅ |
| 15 | Review | Get by id | GET /reviews/{id} | 200 | 200 | ✅ |
| 16 | Review | Update | PUT /reviews/{id} | 200 | 200 | ✅ |
| 17 | Review | Delete | DELETE /reviews/{id} | 200 | 200 | ✅ |
| 18 | Review | Get after delete | GET /reviews/{id} | 404 | 404 | ✅ |
| 19 | Review | Invalid rating rejected | POST /reviews/ | 400 | 400 | ✅ |
| 20 | Review | Empty text rejected | POST /reviews/ | 400 | 400 | ✅ |
| 21 | Review | Nonexistent user_id rejected | POST /reviews/ | 400 | 400 | ✅ |

**Total: 21/21 tests passed.**

---

## 8. Conclusion

All four entities (Users, Places, Amenities, Reviews) support their required CRUD operations correctly through the Presentation layer (Flask + flask-restx), with the Facade correctly mediating access to the Business Logic and Persistence layers. Validation logic rejects invalid input (out-of-range ratings, empty required fields, duplicate emails, nonexistent related entities) with appropriate `400` status codes instead of crashing. Extended serialization for Place correctly nests full Owner details and the Amenities list, per the project's requirement. Swagger documentation at `/api/v1/` accurately reflects all four registered namespaces.

Three bugs were identified and fixed during testing (see Section 6): an indentation error, a circular import, and a missing return value in `update_user`. All are resolved and verified against the running server.

