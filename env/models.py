from pydantic import BaseModel

class Observation(BaseModel):
    text: str

class Action(BaseModel):
    priority: str

class Reward(BaseModel):
    value: float