import json
from functions import get_best_supplier, get_best_price
from llm_selector import call_tool_from_query, get_final_response

def main():
    user_query = input("Ask your question: ")

    history = [{"role": "user", "content": user_query}]

    available_funcs = {
        "get_best_supplier": get_best_supplier,
        "get_best_price": get_best_price
    }

    task_completed_successfully = False
    while True:
        print("\n--- Thinking... ---")
        tool_calls = call_tool_from_query(history)

        # STOP CONDITION 1: LLM decided to stop
        if not tool_calls:
            # If the history has more than one entry, it means tools were called and we can summarize.
            if len(history) > 1:
                print("\n--- Task Complete ---")
                task_completed_successfully = True
            else:
                print("\n--- Error ---")
                print("I couldn't determine which tool to use based on your query. Please be more specific.")
            break

        # VALIDATION STEP: Ensure all tool calls have a valid part_name
        has_invalid_call = False
        for tool_call in tool_calls:
            args = tool_call.get("arguments", {})
            part_name = args.get("part_name")
            # Check for missing, empty, or placeholder values
            if not part_name or not part_name.strip() or part_name in ["<value>", "part_name"]:
                print("\n--- Error: Missing Information ---")
                print("I need a part name to continue. Please try again and specify which part you're interested in.")
                has_invalid_call = True
                break
        
        # STOP CONDITION 2: Validation failed
        if has_invalid_call:
            break

        print(f"\n--- Executing {len(tool_calls)} Tool(s) ---")
        # Execute all tool calls and gather results
        tool_outputs = []
        for tool_call in tool_calls:
            tool_name = tool_call.get("name")
            args = tool_call.get("arguments", {})
            
            if tool_name in available_funcs:
                print(f"Calling: {tool_name}(**{args})")
                result = available_funcs[tool_name](**args)
                print(f"Result: {result}")
                tool_outputs.append({
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": json.dumps(result)
                })
            else:
                print(f"Error: Tool '{tool_name}' not found.")

        # Add all tool outputs to the history for the next iteration
        history.extend(tool_outputs)

    # Final summary step (only if the task was completed successfully)
    if task_completed_successfully:
        print("\n--- Generating Final Answer ---")
        final_answer = get_final_response(history)
        print("\nFinal Answer:")
        print(final_answer)

if __name__ == "__main__":
    main()
