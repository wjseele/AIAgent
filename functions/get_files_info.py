import os

def get_files_info(working_directory, directory=None):
    try:
        working_path = os.path.abspath(working_directory)
    except Exception as e:
        return f"Error: {e}"
    try:
        directory_path= os.path.join(working_path, directory)
    except Exception as e:
        return f"Error: {e}"    

    if not os.path.isdir(directory_path):
        return f'Error: "{directory}" is not a directory'

    if not directory_path.startswith(working_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    try:
        contents = os.listdir(path=directory_path)
    except Exception as e:
        return f"Error: {e}"

    dir_contents_list = []
    for thing in contents:
        thing_path = os.path.join(directory_path, thing)
        item = f"- {thing}: file_size={os.path.getsize(thing_path)}, is_dir={os.path.isfile(thing_path)}"
        dir_contents_list.append(item)

    dir_contents = "\n".join(dir_contents_list)

    return dir_contents
