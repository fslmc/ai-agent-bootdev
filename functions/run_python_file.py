import os
import subprocess
from subprocess import CalledProcessError

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Function to execute an existing python file, with optional arguments for the python file to be run.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to the specific file to be run, relative to the working directory (default is the working directory itself)",
                },
                "args" : {
                    "type": "Array of string",
                    "description": "The string of arguments to be passed when running the specified file. Optional"
                }
            },
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
        if os.path.commonpath([absolute_path, target_file]) != absolute_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args:
            command.extend(args)

        run = subprocess.run(command, capture_output=True, timeout=30, text=True)

        run.check_returncode()

        if not run.stdout and not run.stderr:
            return "No output produced"

        return f"STDOUT: {run.stdout};\nSTDERR: {run.stderr}"

    except FileNotFoundError as e:
        return f"Error: file not found\n{e}"
    except CalledProcessError:
        return "Process exited with code X"
    except PermissionError as e:
        return f"Error: directory permission error\n{e}"
