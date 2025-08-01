from groq import Groq
from fetch_docstring import tools
import json

class LLMSelector:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.tools = self._prepare_tools(tools)

    def _load_prompt(self):
        with open("prompt.txt", "r") as f:
            return f.read()

    def _prepare_tools(self, tool_list):
        for tool in tool_list:
            tool["parameters"] = {
                "type": "object",
                "properties": {"part_name": {"type": "string"}},
                "required": ["part_name"]
            }
        return tool_list

    def call_tool_from_query(self, history: list):
        base_prompt = self._load_prompt()
        prompt = base_prompt.replace("{history}", json.dumps(history, indent=2)).replace("{tools}", json.dumps(self.tools, indent=2))

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant", # Changed model to a more general tool-calling model
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        
        raw = response.choices[0].message.content.strip()
        print(f"LLM Raw Response: {raw}")
        tool_calls = []

        try:
            # Find the start and end of the JSON list
            start_index = raw.find('[')
            end_index = raw.rfind(']') + 1
            json_str = raw[start_index:end_index]
            tool_calls = json.loads(json_str)
        except (json.JSONDecodeError, IndexError):
            # Handle cases where the response is not a valid JSON
            print("Error: Could not decode LLM response as JSON.")
            pass

        return tool_calls

    def get_final_response(self, history: list) -> str:
        summarization_prompt = f"""
        You are a helpful assistant.
        Based on the following conversation history, please provide a clear and concise summary to the user.
        Combine the information from the tool calls into a single, easy-to-read answer.

        Conversation History:
        {json.dumps(history, indent=2)}

        Final Answer:
        """

        response = self.client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": summarization_prompt}],
            temperature=0.7
        )

        return response.choices[0].message.content.strip()
