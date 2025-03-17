import requests
import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

def get_career_advice(skills, interests):
    """
    Generate career advice using the DeepSeek API.
    """
    if not deepseek_api_key:
        return "Error: Missing DeepSeek API key."

    url = "https://api.deepseek.com/generate"
    headers = {
        "Authorization": f"Bearer {deepseek_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": f"Suggest careers for skills: {skills} and interests: {interests}.",
        "max_tokens": 500
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raises an error for non-200 responses
        
        data = response.json()
        career_advice = data.get("text")

        return career_advice if career_advice else "No career suggestions available."
    
    except requests.exceptions.RequestException as req_err:
        return f"API request error: {str(req_err)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
