import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from get_available_functions import get_available_functions

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    model_name = "gemini-2.0-flash-001"

    if len(sys.argv) < 2:
        print("Usage: python3 main.py <prompt>")
        sys.exit(1)

    user_prompt = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    verbose = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose = True

    available_functions = get_available_functions()

    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    if response.function_calls:
        function_call_part = response.function_calls[0]
        function_call_result = call_function(function_call_part, verbose)
        if not function_call_result.parts[0].function_response.response:
            raise Exception("Nothing returned")
        elif verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
    elif response.text and verbose:
        print(response.text)
    else:
        print("No response text or function calls received.")

    if response.usage_metadata:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def call_function(function_call_part, verbose=False):
    functions_dict = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    function_name = function_call_part.name

    if function_name not in functions_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_args = function_call_part.args
    function_args["working_directory"] = "./calculator"
    actual_function = functions_dict[function_name]
    function_result = actual_function(**function_args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )

main()
