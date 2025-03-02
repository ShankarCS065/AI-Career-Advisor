import streamlit as st
import requests

# Use "backend" instead of "localhost" when running in Docker
BACKEND_URL = "http://fastapi-backend:8000"

def get_career_suggestions(skills, interests):
    """Fetch career suggestions from the backend API."""
    endpoint = f"{BACKEND_URL}/suggest"
    payload = {"skills": skills, "interests": interests}
    
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
        return response.json().get("suggestions", [])
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error: Unable to get suggestions from the server.\n{e}")
        return []

def main():
    st.set_page_config(page_title="AI Career Advisor", page_icon="🚀")
    st.title("🚀 AI Career Advisor")
    st.write("Enter your skills and interests below to receive personalized career suggestions.")
    
    with st.form("career_form"):
        user_skills = st.text_input("Your Skills (comma-separated)", placeholder="e.g., Python, Machine Learning, Web Development")
        user_interests = st.text_input("Your Interests (comma-separated)", placeholder="e.g., AI, Cybersecurity, Finance Tech")
        submitted = st.form_submit_button("Get Suggestions")
    
    if submitted:
        if user_skills.strip() and user_interests.strip():
            suggestions = get_career_suggestions(user_skills, user_interests)
            
            if suggestions:
                st.subheader("🎯 Career Recommendations")
                for idx, suggestion in enumerate(suggestions, start=1):
                    st.write(f"{idx}. {suggestion}")
            else:
                st.info("ℹ️ No suggestions available. Try refining your skills and interests.")
        else:
            st.warning("⚠️ Please fill out both skills and interests.")

if __name__ == "__main__":
    main()
