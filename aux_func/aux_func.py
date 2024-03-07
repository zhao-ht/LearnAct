import re
import ast
from contextlib import contextmanager
import signal
import astor
from re import findall, DOTALL
import threading
import pandas as pd


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


class TimeoutError(Exception):
    pass


def run_with_timeout(func, args=(), kwargs={}, timeout=10):
    """
    Run a function with the given args and kwargs,
    and wait for at most 'timeout' seconds for it to finish.
    If the function doesn't finish in time, raise a TimeoutError.
    """
    result = None
    exception = None

    def worker():
        nonlocal result, exception
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            exception = e

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join(timeout=timeout)
    if thread.is_alive():
        raise TimeoutError(
            f"Function '{func.__name__}' timed out after {timeout} seconds"
        )

    if exception:
        raise exception
    return result


def execute_basic(code_str, global_env={}):
    # local_env = {}
    # try:
    # with time_limit(time_limit_query):
    exec(code_str, global_env)
    return global_env

    # except:
    #     print('execute time error')
    #     return global_env


def execute(code_str, time_limit_query=10, global_env={}):
    return run_with_timeout(
        execute_basic, args=(code_str, global_env), timeout=time_limit_query
    )


def pd_concat_ignore2(df1, df2):
    if len(df1) > 0:
        index_start = df1.index.max() + 1
    else:
        index_start = 0
    return pd.concat(
        [
            df1,
            df2.set_index(
                pd.RangeIndex(start=index_start, stop=index_start + len(df2))
            ),
        ]
    )


def to_number(obj):
    if isinstance(obj, str):
        return eval(obj)
    else:
        return obj


def is_function_called(code_string, function_name):
    try:
        # Parse the code string into an abstract syntax tree (AST)
        tree = ast.parse(code_string)

        # Define a visitor class to search for function calls
        class FunctionCallVisitor(ast.NodeVisitor):
            def __init__(self):
                self.function_called = False

            def visit_Call(self, node):
                if isinstance(node.func, ast.Name) and node.func.id == function_name:
                    self.function_called = True
                self.generic_visit(node)

        # Create an instance of the visitor and visit the AST
        visitor = FunctionCallVisitor()
        visitor.visit(tree)

        return visitor.function_called
    except SyntaxError:
        # Handle syntax errors in the code string
        return False


def is_function_redefined(code_string, function_name):
    try:
        # Parse the code string into an Abstract Syntax Tree (AST)
        parsed_code = ast.parse(code_string)

        # Initialize a set to store the names of functions defined in the code
        defined_functions = set()

        # Traverse the AST to find function definitions
        for node in ast.walk(parsed_code):
            if isinstance(node, ast.FunctionDef):
                defined_functions.add(node.name)

        # Check if the function_name is in the set of defined functions
        return function_name in defined_functions
    except SyntaxError:
        # Handle syntax errors in the code string
        return False


def extract_functions(python_code):
    node = ast.parse(python_code)
    functions = []
    for item in node.body:
        if isinstance(item, ast.FunctionDef):
            func_name = item.name
            func_source = astor.to_source(item)
            functions.append((func_name, func_source))
    return functions


def parse_imported_packages(python_code):
    parsed_code = ast.parse(python_code)

    # Initialize a list to store the imported packages/modules
    imported_packages = []

    # Traverse the AST to find import statements
    for node in ast.walk(parsed_code):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_packages.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module
            for alias in node.names:
                imported_packages.append(f"{module_name}.{alias.name}")
    return imported_packages


def extract_import_lines(python_code):

    # # Define a regular expression pattern to match import statements with dots and "as"
    # pattern = r"^(?:import\s+\w+(?:\.\w+)?(?:\s+as\s+\w+)?|from\s+\w+\s+import\s+\w+(?:\s+as\s+\w+)?)"

    # # Find all matching lines in the code string
    # import_lines = re.findall(pattern, python_code, re.MULTILINE)

    # return import_lines
    lines = python_code.split("\n")
    import_lines = [
        line
        for line in lines
        if line.strip().startswith(("import ", "from ")) and "import" in line
    ]
    return import_lines


def extract_function_name(python_code):
    pattern = r"^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\):"
    func_names = re.findall(pattern, python_code, re.MULTILINE)
    return func_names


def insert_docstring(func_str, docstring):
    # Regular expression pattern to find the def line
    def_pattern = re.compile(r"^\s*def\s+\w+\s*\([^)]*\):", re.MULTILINE)

    # Find the first occurrence of the def line
    match = def_pattern.search(func_str)
    if match:
        # Get the position of the match
        start, end = match.span()

        # Construct the new function string with the docstring
        new_func_str = (
            func_str[:end] + "\n" + '    """' + docstring + '"""\n' + func_str[end:]
        )

        return new_func_str
    else:
        # If no def line is found, return the original function string
        return func_str


def get_decimal_places(number):
    # Convert the number to a string
    number_str = str(number)

    # Check if there is a decimal point in the string
    if "." in number_str:
        # Find the position of the decimal point
        decimal_point_index = number_str.index(".")

        # Calculate the number of decimal places
        decimal_places = len(number_str) - decimal_point_index - 1

        return decimal_places
    else:
        # If there is no decimal point, return 0
        return 0


def get_significant_digits(number):
    # Convert the number to a string to count significant digits
    number_str = str(number)

    # Remove leading and trailing zeros (not significant)
    number_str = number_str.lstrip("0")

    # Count the significant digits
    count = len(number_str.replace(".", "").replace("-", ""))

    return count


def integer_length_of_float(n):
    if -1 < n < 1:
        return 0
    # Get the integer part of the float
    int_part = abs(int(n))

    # Convert the integer to a string and return its length
    return len(str(int_part))


def convert_res_to_ans_format(res, ans):
    number = max(
        integer_length_of_float(eval(ans)) + 1, get_significant_digits(eval(ans))
    )
    return "{:.{}g}".format(float(res), number)


def remove_sure_reply(reply):

    lines = reply.split("\n")

    # Check if the first line contains "Sure" and remove it if it does
    if "Sure" in lines[0] or "Absolutely" in lines[0]:
        print("Sure reply detected: {}".format(lines[0]))
        lines.pop(0)

    # Recreate the text without the first line
    new_text = "\n".join(lines)

    return new_text


def find_undefined_function(code):
    # Parse the code into an Abstract Syntax Tree (AST)
    parsed_code = ast.parse(code)

    # Sets to keep track of undefined and defined functions
    undefined_functions = set()
    defined_functions = set()
    imported_functions = set()

    def find_defined_functions(node):
        # Add locally defined functions and their arguments to the set
        if isinstance(node, ast.FunctionDef):
            defined_functions.add(node.name)
            for arg in node.args.args:
                defined_functions.add(arg.arg)

    def find_imports(node):
        # Add imported functions to the set
        if isinstance(node, ast.ImportFrom):
            for n in node.names:
                imported_functions.add(n.name)

    def find_undefined_functions(node):
        # Check if the function call is to a Name (function or variable)
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                function_name = node.func.id
                if (
                    (function_name not in defined_functions)
                    and (function_name not in imported_functions)
                    and (function_name not in __builtins__)
                ):
                    undefined_functions.add(function_name)

    for node in ast.walk(parsed_code):
        find_defined_functions(node)
        find_imports(node)
        find_undefined_functions(node)

    # Return the undefined functions
    return undefined_functions


def parse_ans(code):
    answer_var = findall(r"\b(ans\s*) =", code, DOTALL)
    return answer_var


def insert_global_env(func_str):
    """
    Adds "global env" statement after the definition line in the given Python function string.

    Args:
    func_str (str): A string representing a Python function.

    Returns:
    str: Modified Python function string with "global env" added.
    """
    # Split the function string into lines
    lines = func_str.split("\n")

    # Identify the line containing the function definition
    # We assume the function definition ends with a colon
    for i, line in enumerate(lines):
        if line.strip().endswith(":"):
            # Insert "global env" after the function definition
            lines.insert(i + 1, "    global env")
            break

    # Reassemble the function string
    modified_func_str = "\n".join(lines)
    return modified_func_str


def parse_python_func(input_str):
    code = "\n\n".join(findall(r"```python\n(.*?)```", input_str, DOTALL))
    return code


def get_func_argument_name(func_str, func_name):
    pattern = r"\b{}\s*\([^)]*\)".format(func_name)
    # Search for the pattern in the function string
    matches = re.findall(pattern, func_str)
    res = matches[0].replace("\n", "").replace("    ", " ")
    return res
