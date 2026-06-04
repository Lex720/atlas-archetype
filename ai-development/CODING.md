# CODING.md

## Python version
Latest stable Alpine variant. Declare in `pyproject.toml`.

## Language
Code, docstrings and comments in **English**.
Exception: error messages returned to the client in **Spanish**.

## Naming
Follow PEP 8 plus:
- Protected: `_single_leading_underscore`
- Private: `__double_leading_underscore`
- Booleans: `is_`, `has_`, `should_` prefix

**Reverse notation** — sequence is module_action_resource_type:
`elements_active` not `active_elements` → `GameCreateUseCase`, `game_create()`, `game_dict`

**Domain simplicity** — simple name inside domain, add context on import:
```python
class GameCreate(ABC): ...  # inside src/domain/game/command/usecase.py
from src.domain.game.command.usecase import GameCreate as GameCreateUsecase
```

## Indentation
4 spaces. Never tabs.

## Imports
Three sections separated by blank line: stdlib → third-party → local.

## Type hints
Mandatory on all public signatures: `def find_user(user_id: str) -> User | None`

## Docstrings
Google style, in English. Document args, returns, raises.

## Return types
Consistent return type. If nullable, declare as `X | None`. Prefer typed objects over dicts or tuples.

## Error handling
- Specific exceptions, never bare `except` or `except Exception` (except at app boundary).
- Fail-fast: validate input early.
- Custom exceptions for domain errors.
- Never `except: pass`.

## Logging
`logger = logging.getLogger(__name__)`. Never `print`. Don't log sensitive data.

## Security
- Never `eval`/`exec` on external input.
- Never `pickle` on untrusted data, use `json`.
- Secrets via env vars, never hardcoded.
- `with` for all resources.

## Testing
- `pytest`. Descriptive names: `test_parse_raises_on_empty_input`.
- Cover: happy path + edge cases + errors.
- Test each use case independently.
- Mock external dependencies (DB, storage).

## General
`ruff` or `black`. Lines ~88-100 chars. No dead code or unresolved `TODO`s. Comment the *why*, not the *what*.
