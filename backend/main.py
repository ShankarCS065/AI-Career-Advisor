import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from data_processing import preprocess_text
from new_features import router as new_features_router

# Load API keys
load_dotenv()
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

if not deepseek_api_key:
    raise ValueError("DEEPSEEK_API_KEY is missing. Check your .env file.")

print("✅ DeepSeek API Key Loaded Successfully.")

# Initialize FastAPI app
app = FastAPI()

# Define request models
class CareerRequest(BaseModel):
    skills: str
    interests: str

class CareerSwitchRequest(BaseModel):
    current_job: str
    experience: int
    skills: str
    interests: str

class WorkLifeBalanceRequest(BaseModel):
    work_hours: int
    stress_level: int
    job_type: str
    vacation_usage: int

# Function to get career advice
def get_career_advice(skills: str, interests: str):
    processed_skills = preprocess_text(skills)
    processed_interests = preprocess_text(interests)

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {deepseek_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a career advisor AI."},
            {"role": "user", "content": f"Suggest careers for someone skilled in {processed_skills} and interested in {processed_interests}."}
        ],
        "max_tokens": 300
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        if "choices" in response_data and len(response_data["choices"]) > 0:
            return response_data["choices"][0].get("message", {}).get("content", "No career suggestions available.")
        else:
            return "⚠️ No valid response from OpenRouter API."

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Function to get career switch advice
def get_career_switch_advice(current_job: str, experience: int, skills: str, interests: str):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {deepseek_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are an AI career transition expert."},
            {"role": "user", "content": f"I am currently a {current_job} with {experience} years of experience. My skills are {skills} and my interests are {interests}. What career transition would you recommend for me?"}
        ],
        "max_tokens": 300
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        if "choices" in response_data and len(response_data["choices"]) > 0:
            return response_data["choices"][0].get("message", {}).get("content", "No career transition advice available.")
        else:
            return "⚠️ No valid response from OpenRouter API."

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Function to get work-life balance advice
def get_work_life_balance_advice(work_hours: int, stress_level: int, job_type: str, vacation_usage: int):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {deepseek_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are an AI work-life balance advisor."},
            {"role": "user", "content": f"I work {work_hours} hours per week, my stress level is {stress_level}/10, my job type is {job_type}, and I have used {vacation_usage} vacation days this year. How is my work-life balance?"}
        ],
        "max_tokens": 500
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        if "choices" in response_data and len(response_data["choices"]) > 0:
            return response_data["choices"][0].get("message", {}).get("content", "No work-life balance suggestions available.")
        else:
            return "⚠️ No valid response from OpenRouter API."

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

@app.get("/")
def root():
    return {"message": "🚀 AI Career Advisor API is running."}

@app.post("/suggest")
def suggest_careers(request: CareerRequest):
    career_suggestions = get_career_advice(request.skills, request.interests)
    
    if "Error:" in career_suggestions:
        raise HTTPException(status_code=500, detail=career_suggestions)

    return {"suggestions": career_suggestions.split("\n")}  

@app.post("/career_switch")
def career_switch(request: CareerSwitchRequest):
    """Get career switch suggestions from API."""
    if not request.current_job or request.experience < 0 or not request.skills.strip() or not request.interests.strip():
        raise HTTPException(status_code=400, detail="Invalid input: Please fill all fields correctly.")

    suggested_career = get_career_switch_advice(request.current_job, request.experience, request.skills, request.interests)

    if "Error:" in suggested_career:
        raise HTTPException(status_code=500, detail=suggested_career)

    return {"suggested_career": suggested_career}

@app.post("/work_life_balance")
def work_life_balance(request: WorkLifeBalanceRequest):
    """Get work-life balance analysis from API."""
    if request.work_hours < 0 or request.stress_level < 1 or request.stress_level > 10 or request.vacation_usage < 0:
        raise HTTPException(status_code=400, detail="Invalid input: Please enter valid values.")

    work_life_advice = get_work_life_balance_advice(request.work_hours, request.stress_level, request.job_type, request.vacation_usage)

    if "Error:" in work_life_advice:
        raise HTTPException(status_code=500, detail=work_life_advice)

    return {"work_life_balance_advice": work_life_advice}

# Include additional features
app.include_router(new_features_router)
