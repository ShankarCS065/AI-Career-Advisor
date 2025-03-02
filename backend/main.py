from fastapi import FastAPI, Body
from model import CareerAdvisorModel
from data_processing import preprocess_text
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# Initialize the CareerAdvisorModel
advisor_model = CareerAdvisorModel()

# Initialize GPT-4 model
llm = ChatOpenAI(temperature=0.7, model_name="gpt-4", openai_api_key=api_key)

@app.get("/")
def root():
    return {"message": "AI Career Advisor API is running."}

@app.post("/suggest")
def suggest_careers(skills: str = Body(...), interests: str = Body(...)):
    """
    API endpoint to suggest careers based on skills and interests.
    """
    # Preprocess input text
    skills_processed = preprocess_text(skills)
    interests_processed = preprocess_text(interests)

    # Get career suggestions from PostgreSQL
    suggestions = advisor_model.suggest_careers(skills_processed, interests_processed)

    # If no careers found, use GPT-4 for AI-based advice
    
    if not suggestions or suggestions == ["No suitable careers found."]:
        prompt = f"Based on the user's skills: {skills} and interests: {interests}, suggest the most suitable career options."
        response = llm.invoke(prompt)
        suggestions = response.content if response else ["No career suggestions available."]
     
    return {"suggestions": suggestions}

