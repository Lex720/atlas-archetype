## APP specifics

This is a **FastAPI** archetype implementing **Clean Architecture + DDD + CQRS**.

### Four-layer structure

```
src/
  domain/          # Business rules — no external dependencies allowed here
  application/     # Use-case implementations + service factories
  infrastructure/  # DB, broker, logger concrete implementations
  presentation/    # Entry points: HTTP API and RabbitMQ consumer
```

The domain defines interfaces (ABCs); infrastructure implements them.

### CQRS split

Every module (`game`, etc.) is split into `command/` (writes) and `query/` (reads). Each side has its own:
- `entity.py` — domain entity (Pydantic model)
- `repository.py` — abstract repository interface
- `usecase.py` — abstract use-case interface (in domain), concrete implementation (in application)

### Service factory pattern

`src/application/<module>/command/service.py` and `query/service.py` act as FastAPI dependency providers. They dynamically import the correct repository implementation at runtime based on `command_motor` / `query_motor` env vars (values: `postgresql` or `mongodb`). This allows using different databases for reads vs. writes.

### Dual-database + ETL replication

When `command_motor != query_motor`, writes published via a command repository also publish an event to RabbitMQ queue `atlas.service_bus`. The consumer (`src/presentation/consumer/__main__.py`) runs as a separate process, and its `replicate_data` handler (`src/presentation/consumer/handlers/etl.py`) replicates the data to the opposite database.

### Two entry points

1. **API** — `src/presentation/api/main.py` → `uvicorn src.presentation.api.main:api`
2. **Consumer** — `src/presentation/consumer/__main__.py` → `python -m src.presentation.consumer`

Both connect to PostgreSQL, MongoDB, and RabbitMQ on startup via the lifespan pattern.

### Adding a new module

Follow the `game` module as the reference template:
1. `src/domain/<module>/` — entities, repository interfaces, use-case interfaces (command + query)
2. `src/application/<module>/` — use-case implementations + service factories
3. `src/infrastructure/database/<technology>/models/<module>/` — ORM models
4. `src/infrastructure/database/<technology>/repositories/<module>/` — repository implementations
5. `src/presentation/api/resources/<module>/` — DTOs + routes; register router in `main.py`
6. Mirror test structure under `tests/unit/` and `tests/e2e/`

## Commands

### Docker deployment
```bash
make build.deployment && make run.deployment  # Build and start api + consumer containers
make logs.api         # Tail API container logs
make logs.consumer    # Tail consumer container logs
make stop.all         # Stop all containers
```

### Testing
```bash
make build.unit-tests && make run.unit-tests    # Unit tests in Docker
make build.e2e-tests && make run.e2e-tests      # E2E tests in Docker (spins up all infra)
make run.coverage-report                        # Full suite + HTML coverage report (threshold: 80%)

# Single test locally
pytest tests/unit/application/game/command/test_usecase.py -v
pytest tests/unit -k "test_name" -v
```

### Migrations (PostgreSQL via Alembic, requires running container)
```bash
make makemigrations name="describe what changes"   # Autogenerate migration file
make migrate                                        # Apply migrations (alembic upgrade head)
```

### Multi-arch build (for GCP GKE or any registry)
```bash
make buildx.setup                                              # Run once per machine to create the multi-arch builder
make build.deployment                                          # Local build — native platform, loads into Docker daemon
make build.deployment.push REGISTRY=gcr.io/my-project TAG=v1  # Multi-arch push (linux/amd64 + linux/arm64)
```

### Manual replication smoke test
Verifies the full ETL flow: write to PostgreSQL → RabbitMQ event → consumer replicates to MongoDB → read from MongoDB.

Default docker-compose config: `COMMAND_MOTOR=postgresql`, `QUERY_MOTOR=mongodb`.

```bash
# 1. Start the app and apply migrations
make build.deployment && make run.deployment
docker exec atlas-api alembic upgrade head   # use docker exec, not make migrate (avoids -t flag issue in non-TTY)

# 2. Write a game (goes to PostgreSQL, publishes event to atlas.service_bus)
curl -s -X POST http://localhost:8080/atlas/game \
  -H "Content-Type: application/json" \
  -d '{"name": "The Last of Us", "platform": "ps", "stock": 10, "price": 60, "active": true, "condition": "new"}'

# 3. Read games (served from MongoDB — confirms replication worked)
curl -s http://localhost:8080/atlas/game | python3 -m json.tool
```

Valid enum values: `platform` → `ps`, `xbox`, `pc` | `condition` → `new`, `used`.

The created game should appear in the GET response within ~1–2 seconds. If it doesn't, check consumer logs: `make logs.consumer`.
