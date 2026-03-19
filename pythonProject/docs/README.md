

# Computer Use Product - Part 1 Skeleton

## Project Structure

The planned project structure:

computer-use-product/
├── api/ # FastAPI backend code
│ ├── **init**.py
│ ├── main.py
│ ├── websocket.py
│ └── routes/
│ ├── sessions.py
│ ├── messages.py
│ └── health.py
├── agent/ # Agent container logic
│ ├── **init**.py
│ ├── agent_manager.py
│ ├── session.py
│ └── utils.py
├── db/ # Database models and CRUD
│ ├── models.py
│ ├── schemas.py
│ └── crud.py
├── docker/ # Docker configuration
│ ├── docker-compose.yml
│ ├── Dockerfile.api
│ └── Dockerfile.agent
├── tests/ # Test cases
│ ├── test_agent.py
│ ├── test_api.py
│ └── test_concurrent_sessions.py
├── requirements.txt
├── README.md
└── plan.md

### Reasoning:

- `api/` contains REST + WebSocket endpoints for sessions and messaging.
- `agent/` manages agent containers and session handling.
- `db/` contains database models, Pydantic schemas, and CRUD operations.
- `docker/` allows local deployment and container orchestration.
- `tests/` provides both REST and WebSocket concurrency tests.
- `requirements.txt` pins all Python dependencies.
- `plan.md` contains step-by-step implementation plan.

---

## Sequence Diagram
