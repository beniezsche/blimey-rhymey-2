from pydantic import BaseModel
from typing import Any

class Headline(BaseModel):
    id: int
    headline: str
    rhyme: str

class SearchResults(BaseModel):
    id: int
    headline: str
    distance: float

# This defines the data json format expected for the endpoint, change as needed
class TextInput(BaseModel):
    inputs: str
    parameters: dict[str, Any] | None

class UserCredentials(BaseModel):
    token: str