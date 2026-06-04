from src.application.healthcheckers.usecase import Check as CheckUseCase
from src.application.healthcheckers.usecase import HealthCheck as HealthCheckUseCase
from src.infrastructure.broker.rabbitmq.repositories.healthchek.query.repository import (  # noqa: E501
    Check as CheckRepositoryRabbitmq,
)
from src.infrastructure.database.mongodb.repositories.healthchek.query.repository import (  # noqa: E501
    Check as CheckRepositoryMongodb,
)
from src.infrastructure.database.postgresql.repositories.healthchek.query.repository import (  # noqa: E501
    Check as CheckRepositoryPostgresql,
)


def postgresql_check() -> CheckUseCase:
    """Return the implementation of postgresql check usecase as a service."""
    return CheckUseCase(CheckRepositoryPostgresql(), "Postgresql")


def mongodb_check() -> CheckUseCase:
    """Return the implementation of mongodb check usecase as a service."""
    return CheckUseCase(CheckRepositoryMongodb(), "Mongodb")


def rabbitmq_check() -> CheckUseCase:
    """Return the implementation of rabbitmq check usecase as a service."""
    return CheckUseCase(CheckRepositoryRabbitmq(), "Rabbitmq")


def health_check() -> HealthCheckUseCase:
    """Return the implementation of health check usecase as a service."""
    return HealthCheckUseCase([postgresql_check(), mongodb_check(), rabbitmq_check()])
