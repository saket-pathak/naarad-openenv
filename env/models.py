from openenv.core import Action as BaseAction, Observation as BaseObservation
from pydantic import BaseModel


class Observation(BaseObservation):
    text: str
    severity_hint: str | None = None


class Action(BaseAction):
    priority: str


class Reward(BaseModel):
    value: float