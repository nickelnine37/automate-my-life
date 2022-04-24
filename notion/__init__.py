from secrets.config import secrets
from notion_client import Client

notion = Client(auth=secrets['notion_token'])