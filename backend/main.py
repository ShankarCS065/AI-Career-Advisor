from fastapi import FastAPI, Body
from model import CareerAdvisorModel
from data_processing import preprocess_text

app = FastAPI()

advisor_model = CareerAdvisorModel()

@app.get("/")
def root():
    return {"message": "AI Career Advisor API is running."}

@app.post("/suggest")
def suggest_careers(skills: str = Body(...), interests: str = Body(...)):
    skills_processed = preprocess_text(skills)
    interests_processed = preprocess_text(interests)
    suggestions = advisor_model.suggest_careers(skills_processed, interests_processed)
    return {"suggestions": suggestions}
