from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.infrastructure.database.postgresql.interface import (
    Postgresql as PostgresqlInterface,
)
from src.infrastructure.database.postgresql.settings import get_settings_postgresql

settings = get_settings_postgresql()


class Postgresql(PostgresqlInterface):
    """Postgresql database configuration with sqlalchemy async engine.

    Note:
        This class inherit from the Postgresql interface (ABC).
    """

    def __init__(self) -> None:
        """Initialize the class with the necessary objects implemented."""
        self.__session: async_sessionmaker | None = None
        self.__engine: AsyncEngine | None = None

    def connect(self, expire_on_commit: bool = False) -> async_sessionmaker:
        """Performs the connection to the database.

        Note:
            Create the async engine that needs to be used to generate the async session.

        Args:
            expire_on_commit (:obj:`bool`): Define if session expires after committing.

        Returns:
            Async session stored in the property of the class.
        """
        self.__engine = create_async_engine(
            settings.postgresql_url,
            echo=settings.sqlalchemy_echo,
            echo_pool=settings.sqlalchemy_echo_pool,
            pool_size=settings.sqlalchemy_pool_size,
            max_overflow=settings.sqlalchemy_max_overflow_pool,
            pool_timeout=settings.sqlalchemy_pool_timeout,
        )

        self.__session = async_sessionmaker(
            bind=self.__engine,
            autocommit=False,
            expire_on_commit=expire_on_commit,
        )
        return self.__session

    async def disconnect(self) -> None:
        """Performs the disconnect from the database.

        Returns:
            None.
        """
        await self.__engine.dispose()

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Yields async session generator.

        Returns:
            Async session generator.
        """
        async with self.__session() as session:
            yield session

    async def get_async_database(self) -> AsyncGenerator[AsyncSession, None]:
        """Gets async session instance.

        Returns:
            Async session instance.
        """
        return self.__session()


postgresql = Postgresql()

TAsyncSession = Annotated[AsyncSession, Depends(postgresql.get_async_session)]
