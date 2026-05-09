import os
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from dependencies import get_current_user

from dotenv import load_dotenv
load_dotenv()

router = APIRouter(prefix="/ai", tags=["AI"])
if not os.getenv("GEMINI_API_KEY"):
    raise RuntimeError("GEMINI_API_KEY is not set in .env")

client = genai.Client()
MODEL_NAME = "gemini-3.1-flash-lite"
GENERATION_CONFIG = types.GenerateContentConfig(
    temperature=0.7,
    max_output_tokens=512,
)

SYSTEM_CONTEXT  = """ You are a helpful python programming assistant for cpllege students learning python full stack development.
Explain concepts Clearly and concisely using simple real-world analogies. Use short code examples when helpfull.
Keep answers befginner friendly and under 200 words unless the question genuinely requires more detail.
RULE: you are not allowed to answer the questions taht are not related to this context."""

class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
class AskResponse(BaseModel):
    answer: str

@router.post("/ask", response_model=AskResponse)
def ask_ai(request: AskRequest,
           current_user= Depends(get_current_user)):
    full_prompt = f"{SYSTEM_CONTEXT}\n\nStudent question: {request.question}"

    try:
        response = client.models.generate_content(

            model= MODEL_NAME,

            contents= full_prompt,
            config= GENERATION_CONFIG,
        )
        return AskResponse(answer= response.text)
    
    except ValueError:
        raise HTTPException( status_code=400,
                            detail=" This question could not be answered. please rephrase it.")
    except Exception as e:
        print(f"Gemini error: {e}")
        raise HTTPException( status_code=503,
                            detail=" AI service is temporarly unavailabe. Try again in a moment.")