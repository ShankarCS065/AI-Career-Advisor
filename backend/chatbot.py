from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize GPT-4 model
llm = ChatOpenAI(temperature=0.7, model_name="gpt-4", openai_api_key=api_key)

# Define prompt template
prompt = PromptTemplate(
    input_variables=["skills", "interests"],
    template="Based on the user's skills: {skills} and interests: {interests}, suggest the most suitable career options."
)

def get_career_advice(skills, interests):
    """
    Generate career advice using GPT-4.
    """
    formatted_prompt = prompt.format(skills=skills, interests=interests)
    response = llm.invoke(formatted_prompt)  # Correct method to call LLM
    return response.content if response else "No career suggestions available."
