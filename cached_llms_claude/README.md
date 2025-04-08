## cached_llms_claude

**Author:** alterxyz
**Version:** 0.0.1
**Type:** tool

### Description

## Example

```python

the_text_1 = """
Really long text here
"""

the_text_2 = """
Really long text here
"""
the_text_3 = """
Really long text here
"""
the_text_4 = """
Really long text here
"""

system = """
[
    {
        "type": "text",
        "text": "You are an AI assistant, we are just testing, just say 'Hello, world' to the user."
    },
    {
        "type": "text",
        "text": the_text_1,
        "cache_control": {"type": "ephemeral"}
    }, {
        "type": "text",
        "text": "Also, end with a exclamation mark."
    },
]
"""

messages = """
[
    {
        "role": "user",
        "content": [
                {
                    "type": "text",
                    "text": "ok,"
                },
            {
                    "type": "text",
                    "text": the_text_2,
                    "cache_control": {"type": "ephemeral"}
                },
            {
                    "type": "text",
                    "text": "Say it!"
                }
        ]
    }
]
"""
```

