from datetime import datetime

import pytest
import pytest_asyncio

from src.application.commons.date_format import datetime_to_isoformat


@pytest.mark.asyncio
class TestDateFormat:
    @pytest_asyncio.fixture(scope="class")
    async def datetime_data(self) -> datetime:
        return datetime.now()

    async def test_datetime_to_isoformat(self, datetime_data: datetime) -> None:
        new_date = datetime_to_isoformat(datetime_data)

        assert isinstance(new_date, str)
