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
    git clone [https://github.com/loicleguen/holbertonschool-hbnb/tree/main/part2](https://github.com/loicleguen/holbertonschool-hbnb/tree/main/part2)
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




---

## Authors
<div align="center">
  
| Author | Role | GitHub | Email |
|--------|------|--------|-------|
| **Loïc Le Guen** | Co-Developer | [@loicleguen](https://github.com/loicleguen) | 11510@holbertonstudents.com |
| **Valentin TIQUET** | Co-Developer | [@vtiquet](https://github.com/vtiquet) | 11503@holbertonstudents.com |
</div>
