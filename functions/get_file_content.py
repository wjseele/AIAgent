import os

def get_file_content(working_directory, file_path):
    try:
        working_path = os.path.abspath(working_directory)
    except Exception as e:
        return f"Error: {e}"
    try:
        file_full_path = os.path.join(working_path, file_path)
    except Exception as e:
        return f"Error: {e}"

    if not file_full_path.startswith(working_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(file_full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    MAX_CHARS = 10001
    try:
        with open(file_full_path, "r") as f:
            file_content = f.read(MAX_CHARS)
    except Exception as e:
        return f"Error: {e}"

    if len(file_content) > 10000:
        file_content = file_content[:-1]
        file_content += f"[...File {file_path} truncated at 10000 characters]"

    return file_content
