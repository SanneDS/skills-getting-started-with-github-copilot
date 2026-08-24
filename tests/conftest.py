"""Shared pytest fixtures for the FastAPI backend tests."""
import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities as activities_db
from src.app import app

ORIGINAL_ACTIVITIES_STATE = copy.deepcopy(activities_db)


@pytest.fixture
def client(reset_activities):
    """A TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities database before and after each test.

    The app stores activity data in a module-level dict, so tests that
    sign up or unregister students must not leak state between tests.
    """
    activities_db.clear()
    activities_db.update(copy.deepcopy(ORIGINAL_ACTIVITIES_STATE))
    yield
    activities_db.clear()
    activities_db.update(copy.deepcopy(ORIGINAL_ACTIVITIES_STATE))
