import os
from dotenv import load_dotenv
from dataclasses import dataclass


load_dotenv()

@dataclass
class Postgres:
    def __init__(self) -> None:
        self.db = os.getenv('POSTGRES_DB')
        self.user = os.getenv('POSTGRES_USER')
        self.password = os.getenv('POSTGRES_PASSWORD')
        self.host = os.getenv('POSTGRES_HOST')
        self.port = os.getenv('POSTGRES_PORT')
