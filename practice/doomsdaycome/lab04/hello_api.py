"""Lab 4 warm-up: your first web API in a few lines.

Run it:
    uvicorn hello_api:app --reload
Then open http://127.0.0.1:8000/docs in your browser.

Exercises P1–P5 are in README.md. Each one adds a few lines at the marked place.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Hello API")


@app.get("/")
def home() -> dict:
    return {"message": "Hello, CSC10014!"}


@app.get("/hello/{name}")
def hello(name: str) -> dict:
    return {"message": f"Hello, {name}!"}


@app.get("/square")
def square(n: int) -> dict:
    return {"n": n, "square": n * n}


class Numbers(BaseModel):
    a: float
    b: float


@app.post("/add")
def add(nums: Numbers) -> dict:
    return {"sum": nums.a + nums.b}


COURSES = {
    "CSC10014": "Computational Thinking",
    "CSC10001": "Fundamentals of Programming",
}


@app.get("/courses/{code}")
def course(code: str) -> dict:
    if code not in COURSES:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"code": code, "name": COURSES[code]}
