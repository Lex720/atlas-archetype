import pytest

from src.application.healthcheckers.interface import CheckRepository
from src.application.healthcheckers.usecase import Check as CheckUseCase
from src.application.healthcheckers.usecase import HealthCheck as HealthCheckUseCase


class CheckMock(CheckRepository):
    async def __call__(self) -> bool:
        return True


@pytest.mark.asyncio
class TestUsecase:
    async def test_health_check_passed(self) -> None:
        check_executor = CheckUseCase(CheckMock(), "checker1")

        check = await check_executor()

        assert check.passed

    async def test_health_check_not_passed(self) -> None:
        check_executor = CheckUseCase(None, "checker1")

        check = await check_executor()

        assert not check.passed

    async def test_health_check_report_passed(self) -> None:
        checker1 = CheckUseCase(CheckMock(), "checker1")
        checker2 = CheckUseCase(CheckMock(), "checker2")

        health_check_executor = HealthCheckUseCase([checker1, checker2])

        health_check_report = await health_check_executor()

        assert health_check_report.healthy
        assert len(health_check_report.checks) == 2

    async def test_health_check_report_not_passed(self) -> None:
        checker1 = CheckUseCase(CheckMock(), "checker1")
        checker2 = CheckUseCase(None, "checker2")

        health_check_executor = HealthCheckUseCase([checker1, checker2])

        health_check_report = await health_check_executor()

        assert not health_check_report.healthy
        assert len(health_check_report.checks) == 2
