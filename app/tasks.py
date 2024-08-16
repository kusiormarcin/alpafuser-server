from celery import Celery, Task, shared_task
import subprocess
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

script_path = os.path.join(current_dir, "../generate.sh")

@shared_task()
def diffuse(prompt: str):
    # Using subprocess with additional script file, because simply running Python code was throwing an error
    result = subprocess.run([script_path, prompt], capture_output=True, text=True)
    return result.stdout.rstrip()