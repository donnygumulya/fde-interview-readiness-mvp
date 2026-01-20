from sqlalchemy import Column, Integer, String, Text
from database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    feedback = Column(Text)
    readiness_score = Column(Integer)
    risks = Column(Text)
    coaching_tips = Column(Text)