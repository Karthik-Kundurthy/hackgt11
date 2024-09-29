from __future__ import annotations
from pymongo import MongoClient

DB_NAME = "voicemirror"
USERS_COLLECTION = "users"

# Users Columns
COL_USERNAME = "username"
COL_PASSWORD = "password"
COL_PERSONA = "personas"
COL_DESCRIPTION = "description"
COL_DOCUMENTS = "documents"

class MongoAdapter:
    def __init__(self, uri: str):
        self.client = MongoClient(uri)
        self.db = self.client[DB_NAME]
        self.users = self.db[USERS_COLLECTION]
        

    def insert_user(self, username: str, hashed_password: str) -> None:
        self.users.insert_one({COL_USERNAME: username, COL_PASSWORD: hashed_password})

    def add_persona(self, username: str, persona_name: str, persona_descr: str, persona_docs: list) -> None:
        self.users.update_one(
            {COL_USERNAME: username},
            {"$set": {COL_PERSONA: persona_name, COL_DESCRIPTION: persona_descr, COL_DOCUMENTS: persona_docs}}
        )
    
    def edit_persona(self, username, persona, description):
        self.users.update_one(
            {COL_USERNAME: username},
            {"$set": {COL_PERSONA: persona, COL_DESCRIPTION: description}}
        )

        pass

    def get_user(self, username: str) -> User:
        user_dict = self.users.find_one({COL_USERNAME: username})
        if user_dict:
            return User.from_dict(user_dict)
        return None
    


class User:
    def __init__(self, username: str, hashed_password: str):
        self.username = username
        self.hashed_password = hashed_password
        self.personas = []
        self.description = ""

    @staticmethod
    def from_dict(user_dict: dict[str, str]) -> User:
        return User(user_dict[COL_USERNAME], user_dict[COL_PASSWORD])
    