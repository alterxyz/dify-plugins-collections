import httpx


def cached_llms_claude(
    anthropic_api_key: str,
    system: list,
    messages: list,
    model: str = "claude-3-7-sonnet-20250219",
    max_token: str = "4096",
    base_url: str = "https://api.anthropic.com/v1/messages",
) -> dict:
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
                api_url, headers=headers, json=payload, timeout=240.0
            )
            response.raise_for_status()
            response_json = response.json()
            response_text = extract_assistant_response(response_json)
            cache_creation_input_tokens = cache_creation_input_token(response_json)
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
    if response and "content" in response and len(response["content"]) > 0:
        return response["content"][0]["text"]
    else:
        return None


def cache_creation_input_token(response):
    if (
        response
        and "usage" in response
        and "cache_creation_input_tokens" in response["usage"]
    ):
        return response["usage"]["cache_creation_input_tokens"]
    else:
        return None


def cache_read_input_token(response):
    if (
        response
        and "usage" in response
        and "cache_read_input_tokens" in response["usage"]
    ):
        return response["usage"]["cache_read_input_tokens"]
    else:
        return None
