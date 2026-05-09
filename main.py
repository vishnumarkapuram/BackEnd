from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import auth, students

import models.user     
import models.student  
from routers import auth, students, ai
from dotenv import load_dotenv
load_dotenv() 

Base.metadata.create_all(bind=engine)
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://student-management-by-vishnu.vercel.app")
app = FastAPI(title="Student Management API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://student-management-by-vishnu.vercel.app",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(ai.router)
@app.get("/")
def root():
    return {"message": "Student API is running"}