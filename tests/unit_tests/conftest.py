import pytest
import pytest_asyncio

from app.clients.db import DatabaseClient
from app.config import Config
from app.schemas.user import FullUserProfile
from app.services.user import UserService
from models.base import engine, recreate_tables


@pytest.fixture(scope="session")
def sample_full_user_profile() -> FullUserProfile:
    return FullUserProfile(
        short_description="short desc",
        long_bio="def",
        username="abc",
        liked_posts=[1, 2, 3],
    )


@pytest.fixture
def _profile_infos():
    val = {
        0: {
            "short_description": "Default bio description",
            "long_bio": "This is default long bio",
        }
    }
    return val


@pytest.fixture
def _users_content():
    val = {
        0: {
            "username": "Def",
            "liked_posts": [7],
        }
    }
    return val


@pytest.fixture(scope="session")
def testing_config() -> Config:
    return Config()  # type: ignore


@pytest_asyncio.fixture
async def testing_db_client(testing_config) -> DatabaseClient:  # type: ignore
    recreate_tables(engine)
    database_client = DatabaseClient(testing_config, ["user", "liked_post"])
    await database_client.connect()
    yield database_client
    await database_client.disconnect()


@pytest.fixture
def user_service(testing_db_client):
    user_service = UserService(testing_db_client)
    return user_service
