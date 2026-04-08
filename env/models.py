from pydantic import BaseModel

class Observation(BaseModel):
    text: str
    severity_hint: str | None = None

class Action(BaseModel):
    priority: str

class Reward(BaseModel):
    value: float