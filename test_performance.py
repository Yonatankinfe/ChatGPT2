import pytest
import os
import time

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

# Define prompts of varying lengths for latency testing
# max_tokens in get_openai_response will also influence response time.
# We are using the default max_tokens=150 from llm_service.py
PERFORMANCE_PROMPTS = {
    "short_prompt": "Hello.",
    "medium_prompt": "Tell me a short interesting fact about the Roman Empire.",
    "long_prompt": "Explain the basic principles of quantum computing in three simple paragraphs, "
                   "assuming the audience has a high school level understanding of physics. "
                   "What are some potential applications of this technology?"
}

# Define a generous latency threshold in seconds.
# This will vary greatly based on network, API load, model, and max_tokens.
# For a simple test, let's set it relatively high, e.g., 15 seconds.
# For critical applications, this would need to be much tighter and based on SLOs.
MAX_ACCEPTABLE_LATENCY_SECONDS = 20.0

@pytest.mark.api_call
@pytest.mark.skipif(not OPENAI_API_KEY_SET, reason="OPENAI_API_KEY environment variable not set.")
@pytest.mark.parametrize("prompt_key, prompt_text", PERFORMANCE_PROMPTS.items())
def test_response_latency(prompt_key, prompt_text):
    """
    Tests the response latency for different prompts.
    Asserts that the latency is within a broadly acceptable range.
    """
    print(f"\nTesting latency for prompt_key: {prompt_key}")
    # print(f"Prompt: {prompt_text[:100]}...") # Print a snippet of the prompt

    start_time = time.time()
    try:
        response = get_openai_response(prompt_text, max_tokens=150) # Using default max_tokens
    finally:
        end_time = time.time() # Ensure end_time is captured even if there's an error

    latency = end_time - start_time

    print(f"Prompt ({prompt_key}) - Length: {len(prompt_text)} chars")
    print(f"Response received (first 50 chars): {response[:50]}...")
    print(f"Latency: {latency:.4f} seconds")

    assert response is not None, "Response should not be None."
    assert len(response.strip()) > 0, "Response should not be empty."
    assert latency >= 0, "Latency should be a non-negative number."
    assert latency <= MAX_ACCEPTABLE_latency_SECONDS, (
        f"Latency for '{prompt_key}' ({latency:.4f}s) exceeded the threshold of "
        f"{MAX_ACCEPTABLE_LATENCY_SECONDS}s."
    )

# To run these tests (assuming OPENAI_API_KEY is set):
# pytest test_performance.py -m api_call -s
# If OPENAI_API_KEY is not set, these tests will be skipped.
# Latency can be highly variable. These tests provide a basic check, not rigorous benchmarking.
# For more stable results, consider running multiple iterations and averaging,
# or using specialized load testing tools.
# The choice of model ("gpt-3.5-turbo-instruct" here) and max_tokens also significantly impacts latency.
