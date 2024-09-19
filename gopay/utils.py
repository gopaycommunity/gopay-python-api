import tomli

def get_project_version():
    with open('../pyproject.toml', 'rb') as file:
        pyproject_data = tomli.load(file)
    return pyproject_data['tool']['poetry']['version']

DEFAULT_USER_AGENT = "GoPay Python " + get_project_version()