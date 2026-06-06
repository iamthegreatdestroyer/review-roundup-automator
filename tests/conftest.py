import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_llm_client():
    client = MagicMock()
    client.generate.return_value = "Mocked generated content for testing."
    return client

@pytest.fixture
def mock_affiliate_manager():
    manager = MagicMock()
    manager.inject_affiliates.return_value = "Mocked content with affiliates."
    manager.get_affiliate_disclosure.return_value = "This is an affiliate disclosure."
    return manager