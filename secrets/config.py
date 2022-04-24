from getpass import getpass
from zipfile import ZipFile
import json
import os


def get_secrets(password: str) -> dict:
    """
    Use a string password to unzip the encrytped file containing API tokens
    """

    with ZipFile('secrets/secrets.json.zip') as zf:
        zf.extractall('secrets', pwd=password.encode())

    with open('secrets/secrets.json', 'r') as f:
        info = json.load(f)

    os.remove('secrets/secrets.json')

    return info


password = getpass()
secrets = get_secrets(password)
