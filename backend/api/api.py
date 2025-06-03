from fastapi import FastAPI
from dotenv import load_dotenv
import os
import cohere
from fastapi.middleware.cors import CORSMiddleware



load_dotenv()

api = os.getenv('api')
co = cohere.Client(api)
app = FastAPI()

@app.post("/")
def generate(chat):

    response = co.generate(
        model='command',
        prompt=f"""
    Explain the following legal clause in simple terms:
    {chat}
    Your answer should be easy to understand by someone with no legal background.
    """,
        max_tokens=200,
    )
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for stricter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)