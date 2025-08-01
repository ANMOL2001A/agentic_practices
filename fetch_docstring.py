import inspect
from functions import get_best_supplier, get_best_price, get_report

# List of all functions that can be used as tools
TOOLS_LIST = [get_best_supplier, get_best_price, get_report]

def get_docstring(func):
    """Extracts the docstring from a function."""
    return inspect.getdoc(func)

tools = [
    {
        "name": func.__name__,
        "description": get_docstring(func),
    }
    for func in TOOLS_LIST
]
