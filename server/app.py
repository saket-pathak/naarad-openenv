from fastapi import FastAPI
from openenv.core import HTTPEnvServer
from env.models import Action, Observation
from server.environment import ComplaintEnvironment

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Naarad OpenEnv is running"}

server = HTTPEnvServer(ComplaintEnvironment, Action, Observation)
server.register_routes(app)