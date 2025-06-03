from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
import cohere
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Define the input model with validation
class ChatRequest(BaseModel):
    text: str = Field(..., min_length=1, description="The legal clause to explain")

# Load environment variables
load_dotenv()
api_key = os.getenv('api')
if not api_key:
    raise ValueError("Cohere API key not found in .env file. Set the 'api' variable.")

# Initialize Cohere client
co = cohere.Client(api_key)
app = FastAPI()

# Add CORS middleware with stricter settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust for your frontend URL
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/")
async def generate(chat: ChatRequest):
    try:
        # Use co.chat instead of co.generate (modern API)
        response = co.chat(
            message=f"""
            Explain the following legal clause in simple terms:
            {chat.text}
            Your answer should be easy to understand by someone with no legal background.
            No more than 100 words
            You will only answer day-to-day queries and not anything too complex if its too complex respond something similar to: "I am an AI assistant made for day-to-day legal thingies and cannot respond to something of this complexity"
            """,
            model='command',
            max_tokens=200,
        )
        # Extract the generated text
        simplified_explanation = response.text
        return {"explanation": simplified_explanation}
    except cohere.CohereAPIError as e:
        raise HTTPException(status_code=400, detail=f"Cohere API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")