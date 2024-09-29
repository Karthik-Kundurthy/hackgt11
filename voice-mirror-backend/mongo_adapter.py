from __future__ import annotations
from pymongo import MongoClient
from typing import Any, Optional

DB_NAME = "voicemirror"
USERS_COLLECTION = "users"

# Users Columns
COL_USERNAME = "username"
COL_PASSWORD = "password"
COL_PERSONA = "personas"
COL_PERSONA_NAME = "name"
COL_PERSONA_DESCRIPTION = "description"

class MongoAdapter:
    def __init__(self, uri: str):
        self.client = MongoClient(uri)
        self.db = self.client[DB_NAME]
        self.users = self.db[USERS_COLLECTION]

    def insert_user(self, username: str, hashed_password: str) -> None:
        self.users.insert_one({COL_USERNAME: username, COL_PASSWORD: hashed_password})

    def add_persona(self, username: str, persona_name: str, persona_description: str) -> None:
        print(username, persona_name, persona_description)
        self.users.update_one(
            {COL_USERNAME: username},
            {
                "$push": {
                    COL_PERSONA: {
                        COL_PERSONA_NAME: persona_name,
                        COL_PERSONA_DESCRIPTION: persona_description
                    }
                }
            }
        )

    def edit_persona(self, username: str, persona_name: str, persona_description: str) -> None:
        self.users.update_one(
            {COL_USERNAME: username, f"{COL_PERSONA}.{COL_PERSONA_NAME}": persona_name},
            {
                "$set": {
                    f"{COL_PERSONA}.$": {
                        COL_PERSONA_NAME: persona_name,
                        COL_PERSONA_DESCRIPTION: persona_description,
                    }
                }
            }
        )

    def get_user(self, username: str) -> Optional[User]:
        user_dict = self.users.find_one({COL_USERNAME: username})
        if user_dict:
            return User.from_dict(user_dict)
        return None


class User:
    def __init__(self, username: str, hashed_password: str, personas: list[Persona] = []):
        self.username = username
        self.hashed_password = hashed_password
        self.personas = personas

    @staticmethod
    def from_dict(user_dict: dict[str, Any]) -> User:
        personas = [Persona.from_dict(persona_dict) for persona_dict in user_dict[COL_PERSONA]]
        return User(user_dict[COL_USERNAME], user_dict[COL_PASSWORD], personas)
    

class Persona:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @staticmethod
    def from_dict(persona_dict: dict[str, Any]) -> Persona:
        return Persona(persona_dict[COL_PERSONA_NAME], persona_dict[COL_PERSONA_DESCRIPTION])
