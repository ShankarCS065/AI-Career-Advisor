from fastapi import APIRouter, Body, HTTPException
import requests
import os
import logging
from dotenv import load_dotenv

# Load API key
load_dotenv()
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

# Ensure API key is available
if not deepseek_api_key:
    raise RuntimeError("\u274c DEEPSEEK_API_KEY is missing from environment variables.")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI router
router = APIRouter()

@router.post("/deepseek_career_advice")
def deepseek_career_advice(skills: str = Body(..., embed=True), interests: str = Body(..., embed=True)):
    """
    Fetch AI-driven career advice from DeepSeek API based on skills and interests.
    """
    if not skills.strip() or not interests.strip():
        raise HTTPException(status_code=400, detail="Skills and interests cannot be empty.")

    url = "https://openrouter.ai/api/v1/chat/completions"  # Updated API URL
    headers = {
        "Authorization": f"Bearer {deepseek_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",  # Specify the model
        "messages": [
            {"role": "system", "content": "You are an expert AI career advisor. Provide detailed career guidance."},
            {"role": "user", "content": f"Suggest careers for someone with skills: {skills} and interests: {interests}."}
        ],
        "max_tokens": 150  # Allow more detailed responses
    }

    try:
        logger.info("\U0001F535 Sending request to DeepSeek API...")
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raises an exception for 4xx or 5xx responses

        data = response.json()
        logger.info(f"\U0001F4AC API Response: {data}")  # Debugging
        career_advice = data.get("choices", [{}])[0].get("message", {}).get("content")

        if not career_advice:
            logger.warning("⚠️ No career suggestions received from DeepSeek API.")
            raise HTTPException(status_code=500, detail="No career suggestions available at the moment.")

        logger.info("✅ Career advice successfully retrieved.")
        return {"career_advice": career_advice}
    
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"\u274c HTTP error from DeepSeek API: {http_err}")
        raise HTTPException(status_code=response.status_code, detail=f"DeepSeek API error: {str(http_err)}")
    
    except requests.exceptions.RequestException as req_err:
        logger.error(f"\u274c Network/API request error: {req_err}")
        raise HTTPException(status_code=500, detail=f"API request error: {str(req_err)}")

    except Exception as e:
        logger.error(f"\u274c Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
