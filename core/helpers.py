import os

from pathlib import Path


class FileSystem:

    @staticmethod
    def get_base_dir():
        current_path = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(current_path, '..')

    @staticmethod
    def join_on_base_directory(path):
        base_dir = FileSystem.get_base_dir()
        return os.path.join(base_dir, path)

    @staticmethod
    def get_file_contents(directory, file_name):
        input_dir = FileSystem.join_on_base_directory(directory)
        with open(os.path.join(input_dir, file_name)) as file:
            input_data = file.read()
        return input_data

    @staticmethod
    def create_directory(directory_path):
        creation_path = FileSystem.join_on_base_directory(directory_path)
        if not os.path.exists(creation_path):
            path = Path(creation_path)
            path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def create_file(directory_path, filename, contents) -> str:
        creation_path = FileSystem.join_on_base_directory(directory_path)
        if not os.path.exists(creation_path):
            path = Path(creation_path)
            path.mkdir(parents=True, exist_ok=True)
        with open(os.path.join(creation_path, filename), "a+") as writer:
            writer.write(contents)
        return os.path.join(directory_path, filename)
