import json
import os
from dotenv import load_dotenv
from functions import get_best_supplier, get_best_price, get_report
from llm_selector import LLMSelector

load_dotenv()

def main():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file")

    llm_selector = LLMSelector(api_key)

    user_query = input("Ask your question: ")

    history = [{"role": "user", "content": user_query}]

    available_funcs = {
        "get_best_supplier": get_best_supplier,
        "get_best_price": get_best_price,
        "get_report": get_report
    }

    task_completed_successfully = False
    while True:
        print("\n--- Thinking... ---")
        tool_calls = llm_selector.call_tool_from_query(history)

        # STOP CONDITION 1: LLM decided to stop
        if not tool_calls:
            if len(history) > 1:
                print("\n--- Task Complete ---")
                task_completed_successfully = True
            else:
                print("\n--- Error ---")
                print("I couldn't determine which tool to use based on your query. Please be more specific.")
            break

        # VALIDATION STEP
        has_invalid_call = False
        for tool_call in tool_calls:
            args = tool_call.get("arguments", {})
            part_name = args.get("part_name")
            if not part_name or not part_name.strip() or part_name in ["<value>", "part_name"]:
                print("\n--- Error: Missing Information ---")
                print("I need a part name to continue. Please try again and specify which part you're interested in.")
                has_invalid_call = True
                break
        
        if has_invalid_call:
            break

        print(f"\n--- Executing {len(tool_calls)} Tool(s) ---")
        tool_outputs = []
        for tool_call in tool_calls:
            tool_name = tool_call.get("name")
            args = tool_call.get("arguments", {})
            
            if tool_name in available_funcs:
                print(f"Calling: {tool_name}(**{args})")
                result = available_funcs[tool_name](**args)
                # Convert dict to a string that looks like a dict, to match the prompt example
                content = str(result) if isinstance(result, dict) else result
                print(f"Result: {result}")
                tool_outputs.append({
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": content
                })
            else:
                print(f"Error: Tool '{tool_name}' not found.")

        history.extend(tool_outputs)

    if task_completed_successfully:
        print("\n--- Generating Final Answer ---")
        final_answer = llm_selector.get_final_response(history)
        print("\nFinal Answer:")
        print(final_answer)

if __name__ == "__main__":
    main()