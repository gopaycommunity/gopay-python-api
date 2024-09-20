import tomli
import os

def get_project_version():
    pyproject_path = os.path.join(os.path.dirname(__file__), 'pyproject.toml')
    with open(pyproject_path, 'rb') as file:
        pyproject_data = tomli.load(file)
    return pyproject_data['tool']['poetry']['version']

DEFAULT_USER_AGENT = "GoPay Python " + get_project_version()