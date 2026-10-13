import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, directory))
        if os.path.commonpath([absolute_path, target_dir]) != absolute_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        dir_items = os.listdir(target_dir)
        item_dict = []
        for item in dir_items:
            record = {}
            full_path = os.path.join(target_dir, item)
            record['name'] = item
            record['file_size'] = os.path.getsize(full_path)
            record['is_dir'] = os.path.isdir(full_path)
            item_dict.append(record)

        strings = [f"- {item['name']}: file_size={item['file_size']}, is_dir={item['is_dir']}" for item in item_dict]

        return "\n".join(strings)
    except FileNotFoundError as e:
        return f"Error: file not found\n{e}"
    except PermissionError as e:
        return f"Error: directory permission error\n{e}"
