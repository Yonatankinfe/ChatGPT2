import pytest
import os

# Attempt to import the service and check for API key
# This setup is similar to test_llm_service.py for consistency
try:
    from llm_service import get_openai_response
    OPENAI_API_KEY_SET = "OPENAI_API_KEY" in os.environ
except EnvironmentError:
    # This happens if llm_service.py raises EnvironmentError due to missing API key at import time
    OPENAI_API_KEY_SET = False
    # Define a dummy function if import fails, so tests can be defined and skipped
    def get_openai_response(prompt: str, model: str = "gpt-3.5-turbo-instruct", max_tokens: int = 150) -> str:
        raise EnvironmentError("OPENAI_API_KEY not set, get_openai_response is not functional.")
except ImportError:
    # This happens if llm_service.py is not found or has other import errors
    OPENAI_API_KEY_SET = False
    def get_openai_response(prompt: str, model: str = "gpt-3.5-turbo-instruct", max_tokens: int = 150) -> str:
        raise ImportError("Failed to import get_openai_response from llm_service.")

# Common prompts for testing
PROMPTS = {
    "simple_question": "What is the color of the sky on a clear day?",
    "translation_request": "Translate the following English text to French: 'Hello, world!'",
    "creative_writing": "Write a very short story (one sentence) about a robot who dreams.",
    "empty_input": "" # Edge case
}

@pytest.mark.api_call
@pytest.mark.skipif(not OPENAI_API_KEY_SET, reason="OPENAI_API_KEY environment variable not set.")
def test_response_not_empty_for_simple_question():
    """Tests that a simple question gets a non-empty response."""
    prompt = PROMPTS["simple_question"]
    response = get_openai_response(prompt)
    assert response is not None, "Response should not be None."
    assert isinstance(response, str), "Response should be a string."
    assert len(response.strip()) > 0, "Response should not be empty or just whitespace."
    print(f"\nPrompt: {prompt}\nResponse: {response}")

@pytest.mark.api_call
@pytest.mark.skipif(not OPENAI_API_KEY_SET, reason="OPENAI_API_KEY environment variable not set.")
def test_translation_request_contains_plausible_translation():
    """
    Tests a translation request.
    Checks if the response contains characters common in French and not just the original text.
    This is a heuristic, not a perfect translation validation.
    """
    prompt = PROMPTS["translation_request"]
    original_phrase = "Hello, world!"
    response = get_openai_response(prompt)
    assert response is not None
    assert len(response.strip()) > 0
    # Heuristic: check for common French characters or words if possible, and ensure it's not identical to the input part.
    # A more robust check might involve looking for specific translated words if the input is fixed.
    assert original_phrase.lower() not in response.lower() or "bonjour" in response.lower() or "salut" in response.lower() or "monde" in response.lower()
    # Check for some characters that might indicate French (could be improved)
    assert any(char in response for char in ['à', 'é', 'è', 'ê', 'ç', 'ù', 'î', 'ô']) or "bonjour" in response.lower()
    print(f"\nPrompt: {prompt}\nResponse: {response}")

@pytest.mark.api_call
@pytest.mark.skipif(not OPENAI_API_KEY_SET, reason="OPENAI_API_KEY environment variable not set.")
def test_creative_writing_prompt_yields_text():
    """Tests a creative writing prompt gets a non-empty response."""
    prompt = PROMPTS["creative_writing"]
    response = get_openai_response(prompt)
    assert response is not None
    assert isinstance(response, str)
    assert len(response.strip()) > 0
    print(f"\nPrompt: {prompt}\nResponse: {response}")

@pytest.mark.api_call
@pytest.mark.skipif(not OPENAI_API_KEY_SET, reason="OPENAI_API_KEY environment variable not set.")
def test_empty_prompt_handling():
    """
    Tests how the model handles an empty prompt.
    OpenAI API might return an error or an empty/generic response.
    Let's assume for now it should return *something* or handle it gracefully.
    The exact behavior might depend on the model and API version.
    For gpt-3.5-turbo-instruct, an empty prompt is an error.
    We should catch the expected API error.
    """
    prompt = PROMPTS["empty_input"]
    # The OpenAI API typically errors on an empty prompt for completion models.
    # If the model/API changes to allow empty prompts and return a default message, this test would need adjustment.
    with pytest.raises(openai.BadRequestError) as excinfo: # Use openai.BadRequestError if that's what your version/model throws
        get_openai_response(prompt)

    assert "prompt" in str(excinfo.value).lower() # Check if the error message mentions the prompt
    assert "empty" in str(excinfo.value).lower() or "blank" in str(excinfo.value).lower()
    print(f"\nPrompt: \"{prompt}\"\nSuccessfully caught expected error for empty prompt: {excinfo.value}")


# To run these tests (assuming OPENAI_API_KEY is set):
# pytest test_io.py -m api_call -s
# The -s flag shows print statements, which can be helpful for observing LLM responses.
# If OPENAI_API_KEY is not set, these tests will be skipped.
# You might also need to `pip install openai` if not already done.
# And ensure `llm_service.py` is in the same directory or Python path.

# Add a dummy variable to use openai.BadRequestError if it was imported
# This is to avoid unused import errors if API key is not set and tests are skipped
if OPENAI_API_KEY_SET:
    try:
        import openai # Re-import inside block to ensure it's available if key is set
    except ImportError:
        pass # Should have been caught by initial import check

    # This is a bit of a hack to make sure openai.BadRequestError is defined for the test
    # even if the initial from llm_service import get_openai_response failed due to API key
    # and we had to define a dummy get_openai_response.
    # A better way would be to structure the imports and API key check more centrally.
    if not hasattr(openai, 'BadRequestError'):
        # If it's still not available, create a dummy for the test to be defined
        class DummyBadRequestError(Exception):
            pass
        openai.BadRequestError = DummyBadRequestError
else:
    # Define a dummy error if openai itself couldn't be imported or API key not set
    # This ensures the `with pytest.raises(openai.BadRequestError)` line doesn't fail
    # before the skip condition is even evaluated.
    class DummyBadRequestError(Exception):
        pass
    # Create a dummy openai module object to attach the error to, to match the `openai.BadRequestError` access pattern
    class DummyOpenAI:
        BadRequestError = DummyBadRequestError
    openai = DummyOpenAI()
