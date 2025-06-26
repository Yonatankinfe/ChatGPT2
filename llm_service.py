import os
import openai

# Initialize the OpenAI client
# It's good practice to handle the API key via environment variables
try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
except KeyError:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set. Please set it before running tests.")

def get_openai_response(prompt: str, model: str = "gpt-3.5-turbo-instruct", max_tokens: int = 150) -> str:
    """
    Sends a prompt to the OpenAI API and returns the model's response.

    Args:
        prompt: The input text to send to the model.
        model: The OpenAI model to use (default: "gpt-3.5-turbo-instruct").
               You might want to adjust this based on your specific needs or access.
        max_tokens: The maximum number of tokens to generate in the response.

    Returns:
        The text response from the model.

    Raises:
        openai.APIError: If there's an issue with the OpenAI API call.
    """
    if not openai.api_key:
        raise EnvironmentError("OpenAI API key not configured correctly.")

    try:
        response = openai.completions.create(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.1 # Lower temperature for more deterministic testable output initially
        )
        return response.choices[0].text.strip()
    except openai.APIError as e:
        print(f"An OpenAI API error occurred: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires OPENAI_API_KEY to be set)
    # This part will only run if you execute the script directly (e.g., python llm_service.py)
    # and is useful for quick manual testing of this module.
    try:
        sample_prompt = "Translate the following English text to French: 'Hello, world!'"
        print(f"Sending prompt: \"{sample_prompt}\"")
        response_text = get_openai_response(sample_prompt)
        print(f"Received response: \"{response_text}\"")

        sample_prompt_2 = "What is the capital of France?"
        print(f"Sending prompt: \"{sample_prompt_2}\"")
        response_text_2 = get_openai_response(sample_prompt_2)
        print(f"Received response: \"{response_text_2}\"")

    except EnvironmentError as e:
        print(e)
    except openai.APIError as e:
        print(f"Could not run example due to API error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during example usage: {e}")
