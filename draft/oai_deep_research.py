from openai import OpenAI # pip install openai

"""
We will have 2 Dify plugin functions:
1. Start New Deep Research Task
2. Get Deep Research Task Response or Status

API Key should be made by provider folder, prompt and task_id should be provided by user inside tools folder.
"""


def openai_deep_research_new(api_key: str, prompt: str, model: str = "o4-mini-deep-research") -> str:
    try:
        prompt = prompt
        client = OpenAI(api_key=api_key)
        resp = client.responses.create(
            model=model,
            # Options: "low", "medium", "high"; o4-mini only support "medium"
            reasoning={
                "effort": "medium",
            },
            input=prompt,
            background=True,
            tools=[
                {
                    "type": "web_search_preview",
                    "user_location": {"type": "approximate"},
                    "search_context_size": "medium",
                }
            ],
            store=True,  # So you can view the log at your OpenAI account: Dashboard -> Logs
        )
        task_id = resp.id
        return str(task_id)

    except Exception as e:
        return str(e)


def openai_deep_research_get_response(api_key: str, task_id: str):
    client = OpenAI(api_key=api_key)
    resp = client.responses.retrieve(task_id)
    if resp.status == "failed":
        raise Exception(
            f"Task {task_id} failed: {resp.error}. Please contact OpenAI for assistance."
        )
    else:
        return resp


def extract_markdown_from_response(resp) -> str:
    """Extracts the markdown content from the deep research API response."""
    if resp.status != "completed":
        return str(resp.status)

    if not hasattr(resp, "output"):
        return "Empty response or no output found."

    for item in resp.output:
        if hasattr(item, "type") and item.type == "message":
            for content_item in item.content:
                if hasattr(content_item, "type") and content_item.type == "output_text":
                    return content_item.text
    return "Empty response or no output found."

# Example usage of the OpenAI Deep Research API
if __name__ == '__main__':
    test_api_key: str = "<YOUR_API_KEY>"
    prompt: str = "Briefly explain the concept of LLM."

    user_input = int(input("Input 1 for test, 2 for get response: "))
    if user_input == 1:
        task_id = openai_deep_research_new(api_key=test_api_key, prompt=prompt)
        print(f"Task ID: {task_id}")
    else:
        task_id = input("Enter your task ID: ")
        result = openai_deep_research_get_response(api_key=test_api_key, task_id=task_id)
        markdown_content = extract_markdown_from_response(result)
        print(markdown_content)

"""
(.venv) alterxyz@JeromedeMacBook-Pro playground % /Users/alterxyz/playground/.venv/bin/python /Users/alterxyz/playground/oai_dr/demo.py
Input 1 for test, 2 for get response: 1
Task ID: resp_686f7aeaab808192ab0c9ed6afed343102e9af8e2de49a09
(.venv) alterxyz@JeromedeMacBook-Pro playground % /Users/alterxyz/playground/.venv/bin/python /Users/alterxyz/playground/oai_dr/demo.py
Input 1 for test, 2 for get response: 2
Enter your task ID: resp_686f7aeaab808192ab0c9ed6afed343102e9af8e2de49a09
queued
(.venv) alterxyz@JeromedeMacBook-Pro playground % 
(.venv) alterxyz@JeromedeMacBook-Pro playground % /Users/alterxyz/playground/.venv/bin/python /Users/alterxyz/playground/oai_dr/demo.py
Input 1 for test, 2 for get response: 2
Enter your task ID: resp_686f65fb8588819b9fa05a0a4113991106fbfb3fa9e01a87
**大模型**通常指参数规模极大（通常达到数十亿甚至上千亿级别）的深度学习模型。这类模型基于复杂的神经网络结构，通过对海量数据进行预训练来学习复杂的模式和特征，因此具备比小模型更强的表达能力和泛化能力。大模型可用于各种复杂任务，如自然语言处理、计算机视觉、语音识别等领域。
(.venv) alterxyz@JeromedeMacBook-Pro playground % 

"""