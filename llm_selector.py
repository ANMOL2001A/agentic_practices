from groq import Groq
from fetch_docstring import tools
import json
import os
groq_api_key = os.getenv("GROQ_API_KEY")



def load_prompt():
    with open("prompt.txt", "r") as f:
        return f.read()
    

def call_tool_from_query(history: list):
    for tool in tools:
        tool["parameters"] = {
            "type": "object",
            "properties": {"part_name": {"type": "string"}},
            "required": ["part_name"]
        }

    base_prompt = load_prompt()
    prompt = base_prompt.replace("{history}", json.dumps(history, indent=2)).replace("{tools}", json.dumps(tools, indent=2))

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    raw = response.choices[0].message.content.strip()
    tool_calls = []  
    try:
        data = json.loads(raw)
        
        if isinstance(data, dict) and "tool_calls" in data:
            potential_calls = data["tool_calls"]
        elif isinstance(data, list):
            potential_calls = data
        else:
            potential_calls = []

        if isinstance(potential_calls, list):
            tool_calls = [call for call in potential_calls if isinstance(call, dict)]

    except json.JSONDecodeError:
        pass

    return tool_calls


def get_final_response(history: list) -> str:
    """Generates a final, human-readable response based on the conversation history."""
    
    summarization_prompt = f"""
    You are a helpful assistant.
    Based on the following conversation history, please provide a clear and concise summary to the user.
    Combine the information from the tool calls into a single, easy-to-read answer.

    Conversation History:
    {json.dumps(history, indent=2)}

    Final Answer:
    """

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": summarization_prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()