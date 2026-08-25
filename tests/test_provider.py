import pytest
from app.providers.router import select_provider

def test_select_provider_valid():
    client = select_provider("groq")
    assert client is not None

def test_select_provider_invalid():
    with pytest.raises(ValueError):
        select_provider("unknown")