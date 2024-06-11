import json
from typing import List
from fastapi import FastAPI , Form, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import requests

app=FastAPI()

#handle error
@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/calc-grade")
async def courses(grade: List[str]=Form(...) , hours: List[float]=Form(...)):

    points=0
    total_hours=0

    grade_to_points = {
        "A+": 100,
        "A": 95,
        "B+": 90,
        "B": 85,
        "C+": 80,
        "C": 75,
        "D+": 70,
        "D": 65,
        "F": 59
    }
    print(hours)
    print(grade)

    for h, g in zip(hours, grade):

            points += grade_to_points[g] * h

            total_hours += h


    gpa = points / total_hours


    return {"message": f"GPA: {gpa:.2f}"}
