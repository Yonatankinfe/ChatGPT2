import pytest
import os

# Try to import the service; skip tests if OPENAI_API_KEY is not set,
# as the service itself will raise an error, and we don't want CI to fail just for that.
try:
    from llm_service import get_openai_response
    OPENAI_API_KEY_SET = "OPENAI_API_KEY" in os.environ
except EnvironmentError:
    OPENAI_API_KEY_SET = False
except ImportError:
    # This case is if llm_service.py itself has an issue that's not EnvironmentError
    # or if the file doesn't exist, though it should by this point.
    OPENAI_API_KEY_SET = False
    def get_openai_response(prompt: str): # Dummy function to allow tests to be defined
        raise ImportError("Failed to import get_openai_response from llm_service")


@pytest.mark.skipif(not OPENAI_API_KEY_SET, reason="OPENAI_API_KEY environment variable not set.")
def test_can_import_service_function():
    """
    Tests that the get_openai_response function can be imported.
    Actual API call tests will be more involved.
    """
    try:
        from llm_service import get_openai_response
        assert callable(get_openai_response)
    except ImportError:
        pytest.fail("Failed to import get_openai_response from llm_service.")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred during import or check: {e}")

# A very basic placeholder test that doesn't call the API.
# We will add actual API call tests in the next steps.
def test_placeholder():
    """
    A placeholder test to ensure pytest runs.
    """
    assert True

# It's good practice to have a marker for tests that call external APIs.
# This allows selectively running or skipping them.
# We'll use this marker in subsequent test files.
# (No test uses it yet in this file)
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "api_call: marks tests that make actual API calls to OpenAI"
    )

# To run this test, you would typically use the command:
# OPENAI_API_KEY="your_actual_api_key" python -m pytest
# Or set the OPENAI_API_KEY in your environment.
# If the API key is not set, the test_can_import_service_function will be skipped.
# The placeholder test will still run.
