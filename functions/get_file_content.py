import os

from config import MAX_FILE_READ_CHARACTERS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Read the content of a specific file relative to the working directory, providing the content of a file in string form with a character limit.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to the specific file, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}



def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
        if os.path.commonpath([absolute_path, target_file]) != absolute_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_FILE_READ_CHARACTERS)
            if f.read(1):
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_FILE_READ_CHARACTERS} characters]'
                )
        f.close()

        return file_content_string


    except FileNotFoundError as e:
        return f"Error: file not found\n{e}"
    except PermissionError as e:
        return f"Error: directory permission error\n{e}"
    except OSError as e:
        return f"Error: file cannot be opened\n{e}"
