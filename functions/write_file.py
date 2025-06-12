import os

def write_file(working_directory, file_path, content):
    try:
        working_path = os.path.abspath(working_directory)
    except Exception as e:
        return f"Error: {e}"
    try:
        file_full_path = os.path.abspath(os.path.join(working_path, file_path))
    except Exception as e:
        return f"Error: {e}"

    if not file_full_path.startswith(working_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(os.path.split(file_full_path)[0]):
        try:
            os.makedirs(os.path.split(file_full_path)[0])
        except Exception as e:
            return f"Error: {e}"

    try:
        with open(file_full_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
