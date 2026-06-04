from dataclasses import dataclass
from typing import List


@dataclass
class CheckResult:
    """Data class for results check."""

    name: str
    passed: bool
    details: str | None = None


@dataclass
class HealthCheckReport:
    """Data class for health report checks."""

    healthy: bool
    checks: List[CheckResult]
