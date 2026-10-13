import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write a new file or overwrite containing string content.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file path to write the file into, relative to the working directory (default is the working directory itself)",
                },
                "content" : {
                    "type": "string",
                    "description": "The argument to pass the string content of the new file into."
                }
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_path, file_path))
        if os.path.commonpath([absolute_path, target_path]) != absolute_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(absolute_path, exist_ok=True)

        with open(target_path, "w") as f:
            f.write(content)
        f.close()

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except FileNotFoundError as e:
        return f"Error: file not found\n{e}"
    except PermissionError as e:
        return f"Error: directory permission error\n{e}"
    except OSError as e:
        return f"Error: file cannot be opened\n{e}"
