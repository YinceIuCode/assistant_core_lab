"""Lab 4 warm-up: your first web API in a few lines.

Run it:
    uvicorn hello_api:app --reload
Then open http://127.0.0.1:8000/docs in your browser.

Exercises P1–P5 are in README.md. Each one adds a few lines at the marked place.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Hello API")


# P1 (already done): the simplest endpoint. Visit http://127.0.0.1:8000/
@app.get("/")
def home() -> dict:
    return {"message": "Hello, CSC10014!"}


# P2: a path parameter. Visit http://127.0.0.1:8000/hello/Lan
@app.get("/hello/{name}")
def hello(name: str) -> dict:
    # P2: the {name} part of the path becomes the function argument
    return {"message": f"Hello, {name}!"}


# P3: a query parameter. Visit http://127.0.0.1:8000/square?n=7
@app.get("/square")
def square(n: int) -> dict:
    # P3: n is read from the query string ?n=7 and converted to int (422 if not a number)
    return {"n": n, "square": n * n}


# P4: a request body. Send JSON {"a": 2, "b": 3} with POST.
class Numbers(BaseModel):
    a: float
    b: float


@app.post("/add")
def add(nums: Numbers) -> dict:
    # P4: FastAPI validates the JSON body into a Numbers object
    return {"sum": nums.a + nums.b}


# P5: errors. Visit http://127.0.0.1:8000/courses/CSC10014 and /courses/XYZ
COURSES = {"CSC10014": "Computational Thinking", "CSC10001": "Fundamentals of Programming"}


@app.get("/courses/{code}")
def course(code: str) -> dict:
    # P5: unknown course -> 404
    if code not in COURSES:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"code": code, "name": COURSES[code]}
