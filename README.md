<div align="center"><img src="https://github.com/ksyv/holbertonschool-web_front_end/blob/main/baniere_holberton.png"></div>

# HBnB - Project
This repository contains the HBnB project, developed in four progressive parts, each building upon the previous to deliver a complete and robust application. The project aims to design, implement, and deploy a scalable web platform with a clear architecture, a secure backend API, and a dynamic user interface.

## Table of Contents :

  - [HBnB - UML](#subparagraph0)
  - [HBnB - BL and API](#subparagraph1)
  - [HBnB - Auth & DB](#subparagraph2)
  - [HBnB - Simple Web Client](#subparagraph3)


## 📦 HBnB - UML
- [0. High-Level Package Diagram.md](https://github.com/loicleguen/holbertonschool-hbnb/blob/develop/part1/0.%20High-Level%20Package%20Diagram.md): a 3-layer architecture (UML Package Diagram) showing layers and the Facade Pattern.
- [1. Detailed Class Diagram for Business Logic Layer.md](https://github.com/loicleguen/holbertonschool-hbnb/blob/develop/part1/1.%20Detailed%20Class%20Diagram%20for%20Business%20Logic%20Layer.md): a detailed UML Class Diagram for the Business Logic layer entities (User, Place, Review, Amenity)
- [2. Sequence Diagrams for API Calls.md](https://github.com/loicleguen/holbertonschool-hbnb/blob/develop/part1/2.%20Sequence%20Diagrams%20for%20API%20Calls.md): four UML Sequence Diagrams to map the flow of information for key API calls across the three layers
- [3. Documentation Compilation.md](https://github.com/loicleguen/holbertonschool-hbnb/blob/develop/part1/3.%20Documentation%20Compilation.md): a compilation of all diagrams and notes into a single, comprehensive Technical Document.

## 🛠 HBnB - BL and API
1.  **Layered Architecture:** Implemented a clean separation of concerns:
    * **Persistence Layer ([`app/persistence`](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/app/persistence)):** Abstracted data storage logic via a generic [`repository`](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/app/persistence/repository.py).
    * **Service Layer ([`app/services`](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/app/services)):** Established a [`facade`](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/app/services/facade.py) for centralized business logic.
    * **API Layer ([`app/api`](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/app/api)):** Defined clear, standard REST endpoints using Flask Blueprints.
2.  **Core Resource Management:** Full **CRUD** (Create, Read, Update, Delete) functionality was implemented for the following resources:
    * [**Users**](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/app/api/v1/users.py)
    * [**Places**](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/app/api/v1/places.py)
    * [**Reviews**](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/app/api/v1/reviews.py)
    * [**Amenities**](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/app/api/v1/amenities.py)
3.  **Environment Setup:** Finalized project configuration [`config.py`](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/config.py) and dependency management [`requirements.txt`](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/requirements.txt).

## 🔐 HBnB - Auth & DB
In this phase, the backend transitioned to a secure, persistent, and scalable architecture:
1. **JWT Authentication & Authorization:** Implemented user authentication using **Flask-JWT-Extended** and secured endpoints with **role-based access control** (RBAC), allowing only administrators to perform critical actions.
2. **SQLAlchemy ORM Integration:** Replaced the in-memory repository with a **SQLAlchemy-based persistence layer**, mapping all entities (`User`, `Place`, `Review`, `Amenity`) to a database (SQLite for development).
3. **Relational Schema Design:** Designed the complete relational schema, including **one-to-many** and **many-to-many** relationships, and visualized the structure using a **Mermaid.js** Entity-Relationship Diagram.
4. **Data Security:** Integrated **Bcrypt** for secure password hashing within the User model.

## 🌐 HBnB - Simple Web Client

In this final phase, the focus shifts to front-end development using **HTML5**, **CSS3**, and **JavaScript ES6**. The goal is to deliver an interactive and user-friendly web interface that communicates seamlessly with the backend API.

### Objectives

- Design and implement a responsive UI based on provided specifications.
- Enable client-side interaction with the backend API using AJAX/Fetch.
- Securely manage user authentication and session via JWT tokens stored in cookies.
- Apply modern web practices for a dynamic, single-page experience.

### Key Features

1. **Design & Structure**  
   - Completed HTML and CSS files to match design specs.
   - Pages: Login, List of Places, Place Details, Add Review.
   - Semantic HTML5 structure and responsive CSS.

2. **Login Functionality**  
   - AJAX login form authenticates via the API.
   - JWT token stored in cookies for session management.
   - Redirects and error handling for user feedback.

3. **Places Listing & Filtering**  
   - Main page fetches and displays all places as cards.
   - Client-side filtering by price and country.
   - Login link visibility adapts to authentication state.

4. **Place Details & Reviews**  
   - Detailed view for each place, including amenities and reviews.
   - Add review form accessible only to authenticated users.

5. **Add Review**  
   - Authenticated users can submit reviews via AJAX.
   - Success/error messages and redirection handled client-side.

### Technical Highlights

- **Fetch API** for all client-server communication.
- **Cookie-based JWT** session management.
- **DOM manipulation** for dynamic content updates.
- **Client-side form validation** and error handling.
- **CORS** configured on the backend to allow secure cross-origin requests.

## Authors
<div align="center">
  
| Author | Role | GitHub | Email |
|--------|------|--------|-------|
| **Loïc Le Guen** | Co-Developer | [@loicleguen](https://github.com/loicleguen) | 11510@holbertonstudents.com |
| **Valentin TIQUET** | Co-Developer | [@vtiquet](https://github.com/vtiquet) | 11503@holbertonstudents.com |
</div>
