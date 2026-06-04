# Atlas skeleton template

- [About](#about-atlas)
- [AI-assisted development](#ai-assisted-development)
- [Stack](#stack)
- [Key design decisions](#key-design-decisions)
- [Structure](#structure)
- [Configuration](#configuration)
- [Testing strategy](#testing-strategy)
- [Try Out](#try-out)
- [Documentation](#documentation)
- [Recommended Practices](#recommended-practices)

## About atlas

FastAPI archetype implementing **Clean Architecture**, **Domain Driven Design**, **CQRS**, and **DTOs**. The project serves as a production-ready template that demonstrates how to structure a Python API with clear separation of concerns, interchangeable infrastructure, and a disciplined approach to testing. The `game` module is the reference implementation — every new module should follow the same structure.

For deeper technical context see [architecture.md](docs/architecture.md).

## AI-assisted development

This project is built with [Claude Code](https://claude.ai/code). The `ai-development/` folder contains the context files Claude reads on every session:

| File | Purpose |
|---|---|
| [`APP.md`](ai-development/APP.md) | Project overview: architecture, entry points, module conventions, and runbook commands |
| [`ARCHITECTURE.md`](ai-development/ARCHITECTURE.md) | Decision table for choosing patterns (Clean Architecture, DDD, CQRS) and rules for data structures per layer |
| [`CODING.md`](ai-development/CODING.md) | Code style: naming, type hints, error handling, logging, security, and testing standards |

These files replace ad-hoc prompting — Claude understands the project constraints before writing any code.

## Stack

| Area | Technology |
|---|---|
| API framework | FastAPI + Uvicorn |
| PostgreSQL | SQLAlchemy 2 (async) + asyncpg + SQLModel |
| MongoDB | Motor + Beanie |
| Message broker | RabbitMQ via aio-pika |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Testing | pytest + pytest-asyncio + pytest-cov |
| Linting | ruff |
| Runtime | Python 3.10+ · Docker · Make |

## Key design decisions

### Clean Architecture + dependency rule
The domain layer has zero imports from infrastructure or presentation. This means all business logic is testable without spinning up a database, and swapping a concrete implementation never requires touching domain code.

### CQRS split
Each module separates command (write) and query (read) paths into independent entities, repository interfaces, and use cases. This decouples the read model from the write model, makes each path independently testable, and allows different databases for reads vs. writes without compromising either.

### Service factory pattern
`src/application/<module>/command/service.py` and `query/service.py` dynamically import the correct repository at runtime based on `command_motor` / `query_motor` environment variables (`postgresql` or `mongodb`). Swapping the database for a module is a config change, not a code change.

### Dual-database + ETL via RabbitMQ
When `command_motor` and `query_motor` differ, every write also publishes an event to the `atlas.service_bus` queue. The consumer process replicates the data to the opposite database. This demonstrates an event-driven sync pattern without coupling the write path to the replication concern.

### Data structures by layer
| Layer | Tool | Reason |
|---|---|---|
| Presentation (request / response) | Pydantic `BaseModel` | External boundary — deserializes and validates untrusted input |
| Application (commands, queries) | `dataclass` | Internal data — no need for Pydantic overhead |
| Domain (entities, value objects) | `dataclass` / `dataclass(frozen=True)` | Business logic lives here; `frozen=True` for value objects (immutable + hashable) |

### Validation placement
- **Format and syntax** (valid email, non-empty field) → input DTO `field_validator`
- **Business rules** (e.g. a defective game cannot be marked active) → domain entity `__post_init__`

This keeps Pydantic responsible for data shape and the domain responsible for invariants.

## Structure

```
src/
  domain/          # Business rules — no external dependencies allowed
  application/     # Use-case implementations + service factories
  infrastructure/  # DB, broker, logger concrete implementations
  presentation/    # HTTP API and RabbitMQ consumer entry points
tests/
  unit/            # Business logic tests — no external dependencies, fast
  e2e/             # Full-stack tests — no mocks, real infrastructure
```

Detailed directory breakdown:

* [`src`](./src)
    - [`application`](./src/application)
        - [`commons`](./src/application/commons) — shared helpers and utilities
        - [`healthcheckers`](./src/application/healthcheckers) — health check use-case implementations
        - [`*module*`](./src/application/module) — concrete implementations of domain use-case interfaces
    - [`domain`](./src/domain)
        - [`*module*`](./src/domain/module)
            - [`command`](./src/domain/module/command) — entities, repository interfaces, use-case interfaces for writes
            - [`query`](./src/domain/module/query) — entities, repository interfaces, use-case interfaces for reads
    - [`infrastructure`](./src/infrastructure)
        - [`broker`](./src/infrastructure/broker) — broker technology implementations
        - [`database`](./src/infrastructure/database)
            - [`*technology*`](./src/infrastructure/database/technology/)
                - [`models`](./src/infrastructure/database/technology/models) — ORM models grouped by module
                - [`repositories`](./src/infrastructure/database/technology/repositories) — repository implementations grouped by module
        - [`logger`](./src/infrastructure/logger) — logger configuration
    - [`presentation`](./src/presentation)
        - [`api`](./src/presentation/api)
            - [`commons`](./src/presentation/api/commons) — shared DTOs and exception handlers
            - [`resources`](./src/presentation/api/resources) — routes and DTOs per module
        - [`consumer`](./src/presentation/consumer)
            - [`handlers`](./src/presentation/consumer/handlers) — consumer process logic

## Configuration

Two environment variables control which database engine to use for each operation type:

- `command_motor`: database engine for write and delete operations (`postgresql` or `mongodb`)
- `query_motor`: database engine for read operations (`postgresql` or `mongodb`)

This makes it possible to use PostgreSQL for writes and MongoDB for reads, or the same engine for both.

**ETL replication:** when `command_motor` and `query_motor` differ, both repository implementations publish to the `atlas.service_bus` RabbitMQ queue. Starting the consumer process activates the ETL handler, which replicates data to the opposite database automatically. Failed messages retry up to 3 times (configurable via `rabbitmq_max_retries`) with a delay between retries (`rabbitmq_delay_ms`); after exhausting retries the message is sent to a DLQ for inspection.

## Testing strategy

Tests are split into two suites that run in order from fastest to slowest:

- **Unit** — business logic in isolation. No database, no broker, no HTTP. Errors in domain rules are caught here.
- **E2E** — full application stack, no mocks. Tests interact through the real API or consumer interface and validate observable output only. All infrastructure (PostgreSQL, MongoDB, RabbitMQ) runs in Docker.

Coverage threshold: **80%**.

## Try Out

1. Clone the repository:
```bash
git clone ...
```

2. Build and run:
```bash
make build.deployment
make run.deployment
```
The API runs on `localhost:8080`.

To build a multi-arch image and push it to a registry (e.g. for GCP):
```bash
make build.deployment.push REGISTRY=gcr.io/my-project TAG=v1.0.0
```
Run `make buildx.setup` once before the first push to create the multi-arch builder.

3. Follow container logs:
```bash
make logs.api
make logs.consumer
```

4. Run migrations:
```bash
# Generate migration file
make makemigrations name="describe what changes"

# Apply migrations
make migrate
```

5. Stop all containers:
```bash
make stop.all
```

6. Remove Docker images:
```bash
make rmi.deployment
make rmi.linter
make rmi.unit-tests
make rmi.e2e-tests
```

7. Manage dependencies with Poetry:
```bash
# After modifying pyproject.toml
make local.lock
```

8. Run tests:
```bash
# Build and run each suite
make build.unit-tests && make run.unit-tests
make build.e2e-tests && make run.e2e-tests

# Full suite with coverage report
make run.coverage-report
```

9. Local development (without Docker):
```bash
make install       # Install dependencies
make local.lint    # Run linters
make local.test    # Run tests
make local.run     # Start the API
make local.lock    # Update lock file
```

## Documentation

Swagger UI is available at:
```
http://localhost:8080/atlas/docs
```

## Recommended Practices

### Style

Follow [PEP 8](https://peps.python.org/pep-0008/), with the additions below.

#### Naming

- Variables, functions, methods, packages, modules: `lower_case_with_underscores`
- Classes and exceptions: `CapWords`
- Protected methods and internal functions: `_single_leading_underscore`
- Private methods: `__double_leading_underscore`
- Boolean variables: `is_`, `has_`, or `should_` prefix
- Constants: `ALL_CAPS_WITH_UNDERSCORES`

#### Prefer reverse notation

Order: module → action → resource → type.

**Yes**
```python
elements = ...
elements_active = ...
elements_defunct = ...
```

**No**
```python
elements = ...
active_elements = ...
defunct_elements = ...
```

Real examples from this project:

**Classes**
```python
GameCreatePayloadDTO()
GameCreateUseCase()
GameCommandRepository()
```

**Methods**
```python
async def game_create(): ...
async def game_all(): ...
async def health_check_usecase(): ...
```

**Variables**
```python
health_check_report
game_dict
instances_paginated
```

#### Keep class names simple inside their domain

Name a class as simply as possible within its own module, and add context when importing it elsewhere.

Inside `src/domain/game/command/usecase.py`:
```python
class GameCreate(ABC): ...  # "interface" is implicit from the module path
```

When importing outside its domain:
```python
from src.domain.game.command.usecase import GameCreate as GameCreateUsecase

class GameCreate(GameCreateUsecase): ...  # concrete implementation
```

#### Indentation

4 spaces — never tabs.

#### Imports

Three sections separated by a blank line, in this order:

1. Standard library
2. Third-party
3. Local

#### Docstrings

Google style, in English. Document args, return value, and raised exceptions.

```python
def find_game(uuid: str) -> Game | None:
    """Find a game by its unique identifier.

    Args:
        uuid: The game's UUID string.

    Returns:
        The Game entity, or None if not found.

    Raises:
        GameNotFoundError: If the UUID format is invalid.
    """
```
