# CSN Chatbot (MLOps project - momh)

## Overview
This project is a chatbot system for CSN-related questions.
Each team member is responsible for a specific domain:

- Studiestöd
- Återbetalning
- Utlandsstudier

The system is built using Retrieval-Augmented Generation (RAG).


## Architecture
The project consists of:

- Backend (FastAPI + RAG logic)
- Frontend (user interface)
- Docker & Docker Compose for containerization
- GitHub Actions for CI


## How to run

```bash
docker compose up --build
```


## Project Structure

```text
momh/
├── backend/        # API + RAG logic
├── frontend/       # Chat UI
├── docker-compose.yml
└── .github/        # CI workflows
```


## Components

### Backend
Handles:
- RAG pipeline
- API endpoints
- communication with LLM

### Frontend
Handles:
- User interaction
- Sending questions to backend
- Displaying answers

### DevOps
Includes:
- Dockerfiles for services
- docker-compose setup
- CI with GitHub Actions


## Chatbot Domains

Each team member is responsible for a specific CSN domain:

- **Studiestöd** - Handles questions about grants and loans
- **Återbetalning** - Handles repayment-related questions
- **Utlandsstudier** - Handles questions about studying abroad

Each domain has its own RAG pipeline and backend logic but follows a shared API structure for integration.


## Devops & Infrastructure

This project uses containerization and CI to ensure and reproducible environment.

### Docker
- Each service runs in its own container
- backend and frontend are containerized using Dockerfiles

### Docker compose
- Used to run multiple services together
- Simplifies local development and testing

### CI (Github Actions)
- Automatically builds the backend Docker image
- Ensures that the project can run in a clean environment

This setup allows the team to develop independently while maintaining a unified system.


## How to run the project

Make sure Docker is installed and running.

Run the following command:

```bash
docker compose up --build
```

Then open in a browser
http://localhost:8000


## Screenshots
** Placeholder **
Add screenshots here showing the running application


## NOTES

This project demonstrates how independent RAG-based services can be combines into a unified system using DevOps practices.
Each team member works on their own domain while maintaining a shared structure for integration.