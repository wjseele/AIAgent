import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        working_path = os.path.abspath(working_directory)
    except Exception as e:
        return f"Error: {e}"
    try:
        file_full_path = os.path.abspath(os.path.join(working_path, file_path))
    except Exception as e:
        return f"Error: {e}"

    if not file_full_path.startswith(working_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(file_full_path):
        return f'Error: File "{file_path}" not found.'

    if os.path.splitext(file_full_path)[1] != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    try:
        attempt = subprocess.run(["python3", file_full_path], cwd=working_path, capture_output=True, timeout=30)
        if attempt.stdout == b'' and attempt.stderr == b'':
            return "No output produced"

        attempt_result = f"STDOUT: {attempt.stdout.decode()}\nSTDERR: {attempt.stderr.decode()}\n"
        if attempt.returncode != 0:
            attempt_result += f"Process exited with code {attempt.returncode}"
        return attempt_result
    except Exception as e:
        return f"Error: executing Python file: {e}"
