import pytest
import json
from unittest.mock import MagicMock, patch
from main import main
from llm_selector import LLMSelector

@pytest.fixture(autouse=True)
def mock_groq_client():
    with patch('groq.Groq') as mock_groq:
        mock_groq.return_value.chat.completions.create.return_value = MagicMock()
        yield mock_groq

with open('queries.json', 'r') as f:
    test_queries = json.load(f)

@pytest.mark.parametrize("test_case", test_queries)
def test_bot_queries(mock_groq_client, test_case):
    user_query = test_case['query']
    expected_tool_calls = test_case['expected_tool_calls']
    tool_results = test_case['tool_results']
    expected_final_answer = test_case['expected_final_answer']

    # Mock the LLMSelector's call_tool_from_query and get_final_response methods
    llm_selector_instance = LLMSelector("dummy_api_key")
    llm_selector_instance.call_tool_from_query = MagicMock(side_effect=[expected_tool_calls, []]) # First call returns tools, second stops
    llm_selector_instance.get_final_response = MagicMock(return_value=expected_final_answer)

    with patch('main.LLMSelector', return_value=llm_selector_instance):
        with patch('builtins.input', return_value=user_query):
            with patch('builtins.print') as mock_print:
                main()

                # Assert that call_tool_from_query was called with the correct history
                # The first call should have the initial user query
                mock_llm_call_args = llm_selector_instance.call_tool_from_query.call_args_list[0].args[0]
                assert mock_llm_call_args[0]['content'] == user_query

                # If tool calls are expected, check the second call to call_tool_from_query
                if expected_tool_calls:
                    # Assert that get_final_response was called with the correct history
                    final_history_call = llm_selector_instance.get_final_response.call_args_list[0].args[0]
                    
                    # Check if the final answer was printed
                    printed_output = " ".join([call.args[0] for call in mock_print.call_args_list if call.args and isinstance(call.args[0], str)])
                    assert expected_final_answer in printed_output

                # For queries that result in an error (no tool calls), check the error message
                else:
                    printed_output = " ".join([call.args[0] for call in mock_print.call_args_list if call.args and isinstance(call.args[0], str)])
                    assert "I couldn't determine which tool to use based on your query. Please be more specific." in printed_output