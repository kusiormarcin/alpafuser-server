from celery import Celery, Task, shared_task
from celery.result import AsyncResult
from flask import Flask, request
from PIL import Image
from . import tasks
import os
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))

env_path = os.path.join(current_dir, "..",  ".env")

output_path = os.path.join(current_dir, "..", "output")

load_dotenv(env_path)

redis_url = os.getenv("REDIS_URL", "redis://localhost")

def create_app() -> Flask:
    app = Flask(__name__, static_folder=output_path, static_url_path="/output")
    app.config.from_mapping(
        CELERY=dict(
            broker_url=redis_url,
            result_backend=redis_url,
            task_ignore_result=False,
        ),
    )
    celery_init_app(app)

    @app.get("/status/<id>")
    def status(id) -> dict[str, object]:
        result = AsyncResult(id)
        ready = result.ready()
        return {
            "ready": ready,
            "succesful": result.successful() if ready else None,
            "value": result.get() if ready else result.result,
        }

    @app.post("/generate")
    def index() -> dict[str, object]:
        request_data = dict(request.json)
        prompt = request_data["prompt"]
        result = tasks.diffuse.delay(prompt)
        return {
            "request": request_data,
            "result_id": result.id
        }
    
    return app

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)
            
    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app