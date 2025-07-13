## OpenAI Deep Research

### Description

The OpenAI Deep Research plugin is a powerful tool that utilizes the OpenAI API for comprehensive topic research and analysis. This plugin allows users to initiate deep research tasks and retrieve detailed research results upon completion.

### Features

- Create asynchronous deep research tasks
- Check task status
- Retrieve detailed research results
- Supports comprehensive analysis of complex questions and topics

### Tools

This plugin includes two main tools:

1. **Start New Deep Research** (`openai_deep_research`)
   - Creates a new research task based on the user's prompt
   - Returns a task ID for subsequent tracking and result retrieval

2. **Get Deep Research Task Result** (`openai_deep_research_get`)
   - Retrieves the status or result of a research task based on the task ID
   - Shows whether the task is completed, in progress, or has failed

### How to Use

#### Starting a New Research Task

1. Select the "Start New Deep Research" tool
2. Enter a detailed research question or topic
3. After submission, you will receive a task ID

#### Retrieving Research Results

1. Select the "Get Deep Research Task Result" tool
2. Enter the previously obtained task ID
3. View the task status and research results (if completed)

### Usage Example

**Start a research task:**
```
Research Question: "The potential impact and threats of quantum computing on modern cryptography"
Returns: Task ID "resp__abc123xyz"
```

**Get results:**
```
Task ID: "resp_abc123xyz"
Status: "Completed"
Result: [Detailed research report]
```

### Notes

- Complex research tasks may take a long time to complete
- It is recommended to save the task ID for future queries
- The quality of the research results depends on the specificity and clarity of the question provided
- **Currently supports the `o4-mini-deep-research` model**
