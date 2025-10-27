<div align="center"><img src="https://github.com/ksyv/holbertonschool-web_front_end/blob/main/baniere_holberton.png"></div>

# HBNB - API Backend

## 🏠 Project Overview

Welcome to the **HBNB API Backend**! This project is the RESTful API service for the Holberton BNB application, providing all the necessary endpoints for managing users, places, amenities, and reviews.

This structure follows a **layered, modular design** to ensure separation of concerns, maintainability, and scalability. It includes dedicated layers for API handling (`app/api`), business logic/data models (`app/models`), service abstraction (`app/services`), and data persistence (`app/persistence`).

## 📁 Project Structure

The application is structured into several key components:

| Directory | Purpose |
| :--- | :--- |
| `app/api/v1` | **API Endpoints:** Contains the Flask Blueprints for version 1 of the API (e.g., `users.py`, `places.py`, etc.). |
| `app/models` | **Data Models:** Defines the core business entities (e.g., `user.py`, `place.py`). |
| `app/services` | **Service Layer:** Houses the business logic and abstraction via the `facade.py`. |
| `app/persistence` | **Persistence Layer:** Manages data storage and retrieval via the generic `repository.py`. |
| `run.py` | **Entry Point:** The main file to start the Flask application. |
| `config.py` | **Configuration:** Stores application settings, database credentials, etc. |

## 🚀 Getting Started

### Prerequisites

You need **Python 3.x** installed on your system.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/loicleguen/holbertonschool-hbnb/tree/main/part2
    cd hbnb
    ```

2.  **Create and activate a virtual environment** (recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # venv\Scripts\activate    # On Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the API

1.  **Configure:** Ensure your settings are correctly defined in `config.py`.
2.  **Run the application:**
    ```bash
    python3 run.py
    ```
    The API should now be running locally (e.g., at `http://127.0.0.1:5000`).

## 🛠 Usage & API Documentation

The API exposes standard RESTful endpoints.

| Resource | HTTP Method | Example Endpoint | Description |
| :--- | :--- | :--- | :--- |
| **Users** | `GET`, `POST`, `PUT`, `DELETE` | `/api/v1/users` | Manage user accounts. |
| **Places** | `GET`, `POST`, `PUT`, `DELETE` | `/api/v1/places` | Manage rental properties. |
| **Reviews** | `GET`, `POST`, `PUT`, `DELETE` | `/api/v1/reviews` | Manage reviews for places. |
| **Amenities** | `GET`, `POST`, `PUT`, `DELETE` | `/api/v1/amenities` | Manage property features. |


1.  **Create a user:**
```bash
curl -s -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Loic", "last_name": "Leguen", "email": "loic@example.com", "password": "mypassword123"}' \
  | python3 -m json.tool
```
2.  **Create an Amenity:**
```bash
curl -s -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "WiFi"}' \
  | python3 -m json.tool
```
3.  **Create a Place:**
```bash
curl -s -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Appartement Paris", "description": "Beau studio lumineux", "price": 120.0, "latitude": 48.8566, "longitude": 2.3522, "owner_id": "<USER_ID>", "amenities": ["<AMENITY_ID>"]}' \
  | python3 -m json.tool
```
4.  **Create a Review:**
```bash
curl -s -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Superbe séjour!", "rating": 4.5, "user_id": "<USER_ID>", "place_id": "<PLACE_ID>"}' \
  | python3 -m json.tool
```
5.  **Delete a Review:**
```bash
curl -s -X DELETE http://localhost:5000/api/v1/reviews/<REVIEW_ID> | python3 -m json.tool

```

---

## Authors
<div align="center">
  
| Author | Role | GitHub | Email |
|--------|------|--------|-------|
| **Loïc Le Guen** | Co-Developer | [@loicleguen](https://github.com/loicleguen) | 11510@holbertonstudents.com |
| **Valentin TIQUET** | Co-Developer | [@vtiquet](https://github.com/vtiquet) | 11503@holbertonstudents.com |
</div>

