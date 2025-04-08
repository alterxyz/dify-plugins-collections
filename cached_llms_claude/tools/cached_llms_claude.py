from collections.abc import Generator
from typing import Any

from utils.claude import cached_llms_claude

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class CachedLlmsClaudeTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        result = cached_llms_claude(
            anthropic_api_key=tool_parameters["anthropic_api_key"],
            system=tool_parameters["system"],
            messages=tool_parameters["messages"],
            model=tool_parameters["model"],
            max_token=tool_parameters["max_token"],
        )
        text = result["text"]
        cache_creation_input_tokens = result["cache_creation_input_tokens"]
        cache_read_input_tokens = result["cache_read_input_tokens"]
        json_response = result["json"]
        yield self.create_text_message(text)
        yield self.create_variable_message("cache_creation_input_tokens", cache_creation_input_tokens)
        yield self.create_variable_message("cache_read_input_tokens", cache_read_input_tokens)
        yield self.create_json_message(json_response)
