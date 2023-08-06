from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from posts.router import router as posts_router 
from database import database
import requests
from typing import List
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post('/posts/generate-ad-text')
def generate_ad_text(request_data: dict):
    try:
        keywords = request_data.get("keywords")
        if not keywords:
            raise HTTPException(status_code=400, detail="Missing 'keywords' field in request")

        token = os.getenv("TOKEN")
        if not token:
            raise HTTPException(status_code=500, detail="TOKEN not found in environment")

        headers = {
            'Authorization': f"Bearer {token}"
        }

        response = requests.post('https://7583-185-48-148-173.ngrok-free.app/advertisement', headers=headers, json={
            "input_text": keywords
        })

        response.raise_for_status()

        body = response.json()
        generated_text = body.get('output', 'Failed to generate text')

        return {
            "text": generated_text
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Failed to generate text")

app.include_router(posts_router, prefix="/posts", tags=["Posts"])
