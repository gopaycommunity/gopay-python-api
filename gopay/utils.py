from pathlib import Path

import tomli

def get_project_version():
    pyproject_path = Path(__file__).resolve().parent.parent / 'pyproject.toml'
    with open(pyproject_path, 'rb') as file:
        pyproject_data = tomli.load(file)
    return pyproject_data['tool']['poetry']['version']

DEFAULT_USER_AGENT = "GoPay Python " + get_project_version()