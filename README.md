cat << 'EOF' > README.md
# ARGOS Academic Management System

Argos is a modular, event-driven academic management system built using **Python**, **FastAPI**, and **SQLite**.  
It demonstrates advanced concepts in **Object-Oriented Programming**, **Clean Architecture**, **Event Sourcing**, **Scheduling**, and **Concurrent Processing**.

This project fulfills the requirements of the **OOP II Assignment (Advanced Software Architecture & Systems Design)**.

---

## 📌 1. System Overview

Argos models a university-like environment with:

- Students
- Courses
- Sections
- Enrollment Policies
- Facilities (Rooms, Resources)
- Event-Driven Schedulers
- Persistence Layer (SQLite)
- REST API (FastAPI)

The system is built with strict separation between:

common/ → Domain models + core logic
services/ → Application services (Identity, Enrollment, Scheduler)
api/ → REST interface
scripts/ → Developer tools
tests/ → Automated test suite


---

## 📌 2. Key Features

### ✔ Domain-Driven Object Model
Includes:
- AbstractEntity  
- Person hierarchy (Student, Lecturer, Staff, Guest)  
- Course, Section, Syllabus  
- Assessment, Grade  
- Facility/Room/Resource system  

### ✔ Event System
- Event classes  
- EventBus  
- EventStream  
- SQLite-backed EventStore  
- Scheduler reacts to enrollment events  

### ✔ Persistence Layer
- Robust SQLite repositories  
- CRUD operations for Students, Courses, Sections, Enrollments  
- Snapshot storage  

### ✔ Services
- IdentityService  
- EnrollmentService  
- SchedulerService  
- CourseService  
- SectionService  

Each service has:
- Clear interfaces  
- Error handling  
- Logging  
- Thread-safe operations  

### ✔ REST API (FastAPI)
Routes provided:
- `/students`  
- `/enroll`  
- `/health`  

Fully compatible with FastAPI docs at `/docs`.

---

## 📌 3. Installation

### Create virtual environment

python3 -m venv venv
source venv/bin/activate


### Install dependencies

pip install -r requirements.txt
---

## 📌 4. Running the API

make run


The API will run at:



http://127.0.0.1:8000


---

## 📌 5. Database Tools

### Reset the entire database:


make reset-db


### Load demo data:


make demo-data


### Clean caches & test databases:


make clean


---

## 📌 6. Testing

Run all tests:



make test


Run full, verbose tests:



make test-full


The project includes tests for:
- API endpoints  
- Repositories  
- Concurrency  
- Event-stream integrity  

---

## 📌 7. How This Meets the Assignment Requirements

### Object-Oriented Programming Requirements
✔ Abstract classes  
✔ Inheritance (Person → Student, Lecturer, etc.)  
✔ Composition  
✔ Encapsulation via service layers  
✔ Polymorphism (EnrollmentPolicy strategies)  
✔ Versioning & lifecycle logic in AbstractEntity  

### System Architecture Requirements
✔ Multi-layer design (domain → services → API)  
✔ Event-driven architecture  
✔ Scheduler reacting to domain events  
✔ Repository pattern  
✔ Dependency injection  

### Additional Advanced Requirements
✔ Concurrency handling  
✔ Snapshot system  
✔ Logging and monitoring  
✔ Developer scripts & automation  
✔ Full testing suite (pytest)  

---

## 📌 8. Contributing

See `CONTRIBUTING.md` for development workflow.

---

## 📌 9. License

This project is open-source under the MIT License. See `LICENSE` file.

EOF