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

## HBnB - BL and API
1.  **Layered Architecture:** Implemented a clean separation of concerns:
    * **Persistence Layer ([`app/persistence`](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/app/persistence)):** Abstracted data storage logic via a generic [`repository`](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/app/persistence/repository.py).
    * **Service Layer ([`app/services`](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/app/service)):** Established a [`facade`](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/app/service/facade) for centralized business logic.
    * **API Layer ([`app/api`](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/app/api)):** Defined clear, standard REST endpoints using Flask Blueprints.
2.  **Core Resource Management:** Full **CRUD** (Create, Read, Update, Delete) functionality was implemented for the following resources:
    * [**Users**](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/app/api/v1/users.py)
    * [**Places**](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/app/api/v1/places.py)
    * [**Reviews**](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/app/api/v1/reviews.py)
    * [**Amenities**](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/app/api/v1/amenities.py)
3.  **Environment Setup:** Finalized project configuration [`config.py`](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/config.py) and dependency management [`requirements.txt`](https://github.com/loicleguen/holbertonschool-hbnb/blob/main/part2/hbnb/requirements.txt).

## Authors
<div align="center">
  
| Author | Role | GitHub | Email |
|--------|------|--------|-------|
| **Loïc Le Guen** | Co-Developer | [@loicleguen](https://github.com/loicleguen) | 11510@holbertonstudents.com |
| **Valentin TIQUET** | Co-Developer | [@vtiquet](https://github.com/vtiquet) | 11503@holbertonstudents.com |
</div>
