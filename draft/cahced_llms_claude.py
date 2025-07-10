import httpx
import json


def cached_llms_claude(anthropic_api_key: str,  system: list, messages: list, model: str = "claude-3-7-sonnet-20250219", max_token: str = "4096", base_url: str = "https://api.anthropic.com/v1/messages") -> dict:
    api_url = base_url

    headers = {
        "content-type": "application/json",
        "x-api-key": anthropic_api_key,
        "anthropic-version": "2023-06-01",
    }

    payload = {
        "model": model,
        "max_tokens": int(max_token),
        "system": system,
        "messages": messages,
    }

    try:
        with httpx.Client() as client:
            response = client.post(
                api_url, headers=headers, json=payload, timeout=240.0)
            response.raise_for_status()
            response_json = response.json()
            response_text = extract_assistant_response(response_json)
            cache_creation_input_tokens = cache_creation_input_token(
                response_json)
            cache_read_input_tokens = cache_read_input_token(response_json)
            return {
                "text": response_text,
                "cache_creation_input_tokens": str(cache_creation_input_tokens),
                "cache_read_input_tokens": str(cache_read_input_tokens),
                "json": response_json,

            }
    except httpx.TimeoutException:
        raise f"Request timed out after {response.timeout} seconds."
    except httpx.RequestError as e:
        raise f"An error occurred while requesting {e.request.url!r}: {e}"
    except Exception as e:
        raise f"{e}"


def extract_assistant_response(response):
    if response and 'content' in response and len(response['content']) > 0:
        return response['content'][0]['text']
    else:
        return None


def cache_creation_input_token(response):
    if response and 'usage' in response and 'cache_creation_input_tokens' in response['usage']:
        return response['usage']['cache_creation_input_tokens']
    else:
        return None


def cache_read_input_token(response):
    if response and 'usage' in response and 'cache_read_input_tokens' in response['usage']:
        return response['usage']['cache_read_input_tokens']
    else:
        return None


# --- Example Usage ---
if __name__ == "__main__":
    # Get the API key from environment variables for security
    api_key = "<YOUR_API_KEY>"
    the_text = """
Really long text here
"""
    system = [
        {
            "type": "text",
            "text": "You are an AI assistant, we are just testing, just say 'Hello, world' to the user."
        },
        {
            "type": "text",
            "text": the_text,
            "cache_control": {"type": "ephemeral"}
        }, {
            "type": "text",
            "text": "Also, end with a exclamation mark."
        },
    ]

    messages = [
        {
            "role": "user",
            "content": [
                    {
                        "type": "text",
                        "text": "ok,"
                    },
                {
                        "type": "text",
                        "text": the_text,
                        "cache_control": {"type": "ephemeral"}
                    },
                {
                        "type": "text",
                        "text": "Say it!"
                    }
            ]
        }
    ]
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
    else:
        try:
            analysis_result = cached_llms_claude(
                anthropic_api_key=api_key,
                system=system,
                messages=messages,
                model="claude-3-7-sonnet-20250219",
                max_token="4096",
                base_url="https://api.anthropic.com/v1/messages"
            )
            print("API Call Successful. Response:")
            # Pretty print the JSON response
            print(json.dumps(analysis_result, indent=2))

            # Optionally, print just the assistant's response content:
            # if analysis_result and 'content' in analysis_result and analysis_result['content']:
            #    print("\nAssistant's Analysis:")
            #    print(analysis_result['content'][0]['text'])
            """
            {
            "id": "msg_014pUyojMYBKX1M2qp6ykkdN",
            "type": "message",
            "role": "assistant",
            "model": "claude-3-7-sonnet-20250219",
            "content": [
                {
                "type": "text",
                "text": "Hello, world!"
                }
            ],
            "stop_reason": "end_turn",
            "stop_sequence": null,
            "usage": {
                "input_tokens": 7,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 3234,
                "output_tokens": 7
            }
            }
            """

        except Exception as e:
            # Errors are already printed within the function,
            # but we catch here to prevent script crashing.
            print(f"Function call failed: {e}")
