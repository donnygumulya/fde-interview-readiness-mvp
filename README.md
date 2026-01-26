# FDE Interview Readiness Analyzer MVP

This project is a Minimum Viable Product (MVP).  
The goal is to improve candidate success in client interviews by using structured feedback and AI-assisted analysis.

---

## Problem

Candidates who pass internal screening often fail at client interviews due to misalignment between screening criteria and client expectations. Feedback is vague, unstructured, and not systematically used to improve outcomes.

---

## Solution

This MVP provides:

- Standardized feedback ingestion  
- AI-assisted interview readiness scoring  
- Risk factor identification  
- Coaching recommendations for recruiters and candidates  

The system creates a continuous learning loop between internal screening and client interview performance.

---

## Architecture

React Frontend
   ↓
FastAPI Backend (REST API)
   ↓
AI Analysis Layer
   ↓
SQLite Database

## Tech Stack

**Frontend:** React  
**Backend:** Python FastAPI  
**Database:** SQLite  
**AI:** OpenAI API (with fallback logic)  
**Hosting:** AWS (deployment-ready design)

---

## Backend Setup

```bash
cd backend
python -m venv venv
source venv/Scripts/activate
pip install fastapi uvicorn openai python-dotenv
uvicorn main:app --reload
```

Access API docs: http://127.0.0.1:8000/docs

---

## API Example

POST `/analyze`

```json
{
  "candidate_name": "John",
  "feedback": "Candidate is technically strong but struggles to explain solutions clearly."
}
```

RESPONSE:

```json
{
  "readiness_score": 70,
  "risks": ["Communication clarity", "Confidence"],
  "coaching_tips": ["Practice structured explanations", "Mock interview coaching"]
}
```

---

Author

Donny Gumulya
Forward Deployed Engineer Assignment MVP
