from fastapi import FastAPI
from openenv.core import HTTPEnvServer
from env.models import Action, Observation
from server.environment import ComplaintEnvironment
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Naarad OpenEnv is running"}

server = HTTPEnvServer(ComplaintEnvironment, Action, Observation)
server.register_routes(app)


def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()