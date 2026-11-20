# My first web API with FastAPI
#
# An API is a program that other programs (or a browser) can talk to over
# the internet. You visit a URL, and the API sends back data - here, JSON.
#
# This app keeps a small to-do list in memory and lets you:
#   - say hello                          GET    /
#   - greet someone by name              GET    /greet/{name}
#   - see all tasks                      GET    /tasks
#   - see one task                       GET    /tasks/{task_id}
#   - add a task                         POST   /tasks
#   - mark a task as done / rename it    PUT    /tasks/{task_id}
#   - delete a task                      DELETE /tasks/{task_id}
#
# Run it with:   fastapi dev api.py
# Then open:     http://127.0.0.1:8000/docs   (a page to try every route)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Create the app. The title and version show up on the /docs page.
app = FastAPI(title="My First FastAPI App", version="1.0.0")


# ---------------------------------------------------------------------------
# Data shapes
# ---------------------------------------------------------------------------
# A "model" describes what a piece of data must look like.
# FastAPI uses it to check the data people send us. If something is missing
# or has the wrong type, FastAPI replies with an error for us automatically.

class TaskIn(BaseModel):
    """What the user sends when adding or changing a task."""
    title: str
    done: bool = False  # optional - if not sent, it starts as False


class Task(BaseModel):
    """What we send back: the same fields plus an id."""
    id: int
    title: str
    done: bool


# ---------------------------------------------------------------------------
# Our "database"
# ---------------------------------------------------------------------------
# A plain dictionary: the key is the task id, the value is the Task.
# It lives in memory, so it is reset every time the server restarts.

tasks = {
    1: Task(id=1, title="Learn what an API is", done=True),
    2: Task(id=2, title="Build my first FastAPI app", done=False),
}
next_id = 3  # the id the next new task will get


# ---------------------------------------------------------------------------
# Routes (also called "endpoints")
# ---------------------------------------------------------------------------
# @app.get("/path") means: "when someone visits /path with GET, run this".
# Whatever the function returns is turned into JSON for us.

@app.get("/")
def home():
    return {"message": "Welcome to my FastAPI app! Visit /docs to try it out."}


# {name} in the path is a "path parameter" - it comes from the URL itself.
# greeting is NOT in the path, so it is a "query parameter":
#   /greet/Kamal                  -> Hello, Kamal!
#   /greet/Kamal?greeting=Hi      -> Hi, Kamal!
@app.get("/greet/{name}")
def greet(name: str, greeting: str = "Hello"):
    return {"message": f"{greeting}, {name}!"}


# Get all tasks. ?done=true or ?done=false shows only those tasks.
# done can be left out (None), and then every task is returned.
@app.get("/tasks")
def list_tasks(done: bool | None = None):
    result = []
    for task in tasks.values():
        if done is None or task.done == done:
            result.append(task)
    return result


# Get one task. Because task_id is typed as int, FastAPI rejects /tasks/abc.
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks:
        # 404 is the standard code for "not found".
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return tasks[task_id]


# Add a task. The data comes in the request "body" as JSON, for example:
#   {"title": "Practise Python"}
# status_code=201 means "created".
@app.post("/tasks", status_code=201)
def add_task(new_task: TaskIn):
    global next_id  # we want to change the variable defined above

    title = new_task.title.strip()
    if title == "":
        # 400 means "bad request" - the user sent something we can't use.
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    task = Task(id=next_id, title=title, done=new_task.done)
    tasks[next_id] = task
    next_id = next_id + 1
    return task


# Replace a task's title and done status, for example:
#   PUT /tasks/2   with body   {"title": "Build my first FastAPI app", "done": true}
@app.put("/tasks/{task_id}")
def update_task(task_id: int, changes: TaskIn):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    title = changes.title.strip()
    if title == "":
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    tasks[task_id] = Task(id=task_id, title=title, done=changes.done)
    return tasks[task_id]


# Delete a task and send back the one that was removed.
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    removed = tasks.pop(task_id)
    return {"message": "Task deleted", "task": removed}
