from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class FeedbackRequest(BaseModel):
    candidate_name: str
    feedback: str

@app.post("/analyze")
def analyze(data: FeedbackRequest):
    try:
        prompt = f"""
Return JSON ONLY with:
readiness_score (0-100),
risks (array),
coaching_tips (array).

Feedback:
{data.feedback}
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception as e:
        return {"error": str(e)}
