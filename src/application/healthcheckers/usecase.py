import asyncio
from operator import attrgetter
from typing import List

from src.application.healthcheckers.entity import CheckResult, HealthCheckReport
from src.application.healthcheckers.interface import CheckRepository, CheckUsecase


class Check(CheckUsecase):
    """Check usecase implementation for `Check`.

    Note:
        This class inherit from the check usecase interface (ABC).
    """

    def __init__(self, check_repository: CheckRepository, name: str) -> None:
        """Initialize the class with the necessary objects implemented.

        Args:
            __check_repository (:obj:`class`): The repository for health check (private)
            __name (:obj:`str`): The name of the component that needs to be checked.
        """
        self.__check_repository = check_repository
        self.__name = name

    async def __call__(self) -> CheckResult:
        """This method encapsulates all the logic for the check process.

        Returns:
            Check result entity the state of the component.
        """
        try:
            await self.__check_repository()
            return CheckResult(name=self.__name, passed=True)
        except Exception as ex:
            return CheckResult(name=self.__name, passed=False, details=ex.__str__())


class HealthCheck:
    """Health check usecase implementation for `HealthCheck`.

    Note:
        This class inherit from the health check usecase interface (ABC).
    """

    def __init__(self, healthcheckers: List[Check]) -> None:
        """Initialize the class with the necessary objects implemented.

        Args:
            __healthcheckers (:obj:`list`): List of components check implementations.
        """
        self.__healthcheckers = healthcheckers

    async def __call__(self) -> HealthCheckReport:
        """This method encapsulates all the logic for the check report.

        Returns:
            Health check report that contains all individual checks.
        """
        tasks = [check() for check in self.__healthcheckers]
        results = await asyncio.gather(*tasks)

        is_healthy = all(map(attrgetter("passed"), results))

        report = HealthCheckReport(healthy=is_healthy, checks=results)

        return report
