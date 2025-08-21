import pytest
from .factories.user_factory import MemberFactory, BookFactory

@pytest.fixture
def member():
    return MemberFactory()

@pytest.fixture
def book():
    return BookFactory()
