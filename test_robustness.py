import pytest
import os

# Attempt to import the service and check for API key
try:
    from llm_service import get_openai_response
    OPENAI_API_KEY_SET = "OPENAI_API_KEY" in os.environ
except EnvironmentError:
    OPENAI_API_KEY_SET = False
    def get_openai_response(prompt: str, model: str = "gpt-3.5-turbo-instruct", max_tokens: int = 150) -> str:
        raise EnvironmentError("OPENAI_API_KEY not set, get_openai_response is not functional.")
except ImportError:
    OPENAI_API_KEY_SET = False
    def get_openai_response(prompt: str, model: str = "gpt-3.5-turbo-instruct", max_tokens: int = 150) -> str:
        raise ImportError("Failed to import get_openai_response from llm_service.")

@pytest.mark.api_call
@pytest.mark.skipif(not OPENAI_API_KEY_SET, reason="OPENAI_API_KEY environment variable not set.")
def test_response_to_input_with_typos():
    """Tests if the model can handle minor typos and still provide a relevant response."""
    prompt_with_typo = "What is the capitel of Fraance?" # Typos in "capital" and "France"
    expected_topic_word = "Paris" # Assuming it understands and answers correctly

    response = get_openai_response(prompt_with_typo)
    assert response is not None
    assert len(response.strip()) > 0
    # We expect the answer to still be about the capital of France.
    # A simple check could be looking for the correct answer in the response.
    assert expected_topic_word.lower() in response.lower()
    print(f"\nPrompt (with typos): {prompt_with_typo}\nResponse: {response}")

@pytest.mark.api_call
@pytest.mark.skipif(not OPENAI_API_KEY_SET, reason="OPENAI_API_KEY environment variable not set.")
def test_response_to_grammatically_incorrect_input():
    """Tests if the model can handle grammatically incorrect but understandable input."""
    # grammatically incorrect: "How much clocks it is?" instead of "What time is it?"
    # This is a bit abstract. Let's try a more direct question that's just phrased poorly.
    prompt_grammatically_incorrect = "Weather today good or not?"

    response = get_openai_response(prompt_grammatically_incorrect)
    assert response is not None
    assert len(response.strip()) > 0
    # The model might ask for clarification or try its best.
    # We're mainly checking it doesn't crash and gives *some* relevant text.
    # Keywords like "weather", "today", "forecast", "temperature" might appear.
    assert any(keyword in response.lower() for keyword in ["weather", "forecast", "temperature", "conditions", "today's weather"])
    print(f"\nPrompt (grammatically incorrect): {prompt_grammatically_incorrect}\nResponse: {response}")

@pytest.mark.api_call
@pytest.mark.skipif(not OPENAI_API_KEY_SET, reason="OPENAI_API_KEY environment variable not set.")
def test_consistency_with_low_temperature():
    """
    Tests if the model provides consistent (identical or very similar) outputs
    for the same prompt when temperature is low. Our llm_service uses temperature=0.1 by default.
    """
    prompt = "What are three primary colors?"
    num_calls = 3
    responses = []

    for _ in range(num_calls):
        responses.append(get_openai_response(prompt))

    assert len(responses) == num_calls
    for i in range(num_calls):
        assert responses[i] is not None
        assert len(responses[i].strip()) > 0

    # Check if all responses are identical. With very low temperature, they should be.
    # If there are minor, acceptable variations (e.g. an extra space), this assertion might need adjustment.
    first_response = responses[0]
    for i in range(1, num_calls):
        assert responses[i] == first_response, f"Response {i+1} was not identical to the first response.\nResponse 1: {first_response}\nResponse {i+1}: {responses[i]}"

    print(f"\nPrompt (for consistency): {prompt}\nAll {num_calls} responses were identical:\n{first_response}")

# To run these tests (assuming OPENAI_API_KEY is set):
# pytest test_robustness.py -m api_call -s
# If OPENAI_API_KEY is not set, these tests will be skipped.
# Ensure llm_service.py is accessible.
