from getpass import getpass
from utils import get_secrets

password = getpass()
secrets = get_secrets(password)
