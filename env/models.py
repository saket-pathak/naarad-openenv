from openenv.core.env_server.types import Action as BaseAction, Observation as BaseObservation
from pydantic import BaseModel
from typing import Dict, Any


class Observation(BaseObservation):
    model_config = {"arbitrary_types_allowed": True, "validate_assignment": True, "extra": "allow"}
    text: str = ""
    severity_hint: str | None = None


class Action(BaseAction):
    model_config = {"arbitrary_types_allowed": True, "validate_assignment": True, "extra": "allow"}
    priority: str


class Reward(BaseModel):
    value: float