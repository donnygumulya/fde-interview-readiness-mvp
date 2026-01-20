from fastapi import FastAPI
from pydantic import BaseModel
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from database import engine, SessionLocal
from models import Base, Candidate

# Init
Base.metadata.create_all(bind=engine)
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class FeedbackRequest(BaseModel):
    candidate_name: str
    feedback: str

@app.get("/")
def root():
    return {"status": "Backend running"}

@app.post("/analyze")
def analyze(data: FeedbackRequest):

    text = data.feedback.lower()

    try:
        prompt = f"""
        You are evaluating candidate interview readiness.
        Scoring rules:
        - 90-100: Excellent interview readiness
        - 70-89: Good but needs minor improvement
        - 50-69: Moderate readiness, coachable
        - 30-49: High risk
        - 0-29: Very poor readiness

        Return JSON ONLY in this format:
        {{
            "readiness_score": number,
            "risks": [string],
            "coaching_tips": [string]
        }}

        Candidate feedback:
    {text}
    """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        result = response.choices[0].message.content

        result = json.loads(result)

    except Exception as e:
        # Rule-based fallback
        risks = []
        tips = []
        score = 85

        if "communication" in text or "explain" in text:
            risks.append("Communication clarity")
            tips.append("Practice structured explanations")
            score -= 10

        if "confidence" in text or "nervous" in text:
            risks.append("Confidence")
            tips.append("Mock interview coaching")
            score -= 10

        result = {
            "readiness_score": score,
            "risks": risks,
            "coaching_tips": tips,
            "note": "Fallback logic used due to AI quota or API error"
        }

    # store into DB
    db = SessionLocal()
    try:
        candidate = Candidate(
            name=data.candidate_name,
            feedback=data.feedback,
            readiness_score=result["readiness_score"],
            risks=",".join(result["risks"]),
            coaching_tips=",".join(result["coaching_tips"])
        )
        db.add(candidate)
        db.commit()
    finally:
        db.close()

    return result

@app.get("/candidates")
def get_candidates():
    db = SessionLocal()
    try:
        candidates = db.query(Candidate).all()

        return [
            {
                "id": c.id,
                "name": c.name,
                "feedback": c.feedback,
                "readiness_score": c.readiness_score,
                "risks": c.risks.split(","),
                "coaching_tips": c.coaching_tips.split(",")
            }
            for c in candidates
        ]
    finally:
        db.close()
