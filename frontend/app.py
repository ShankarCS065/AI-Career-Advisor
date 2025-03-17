import streamlit as st
import requests
import os

# Load Backend URL from Environment Variables (Default: Docker Backend)
BACKEND_URL = os.getenv("BACKEND_URL", "http://fastapi-backend:8000")

def get_career_suggestions(skills, interests):
    """Fetch career suggestions from the backend API."""
    endpoint = f"{BACKEND_URL}/suggest"
    payload = {"skills": skills, "interests": interests}
    
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json().get("suggestions", [])
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error: Unable to get suggestions from the server.\n{e}")
        return []

def get_career_switch(current_job, experience, skills, interests):
    """Fetch career switch suggestions from the backend API."""
    endpoint = f"{BACKEND_URL}/career_switch"
    payload = {"current_job": current_job, "experience": experience, "skills": skills, "interests": interests}
    
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json().get("suggested_career", "No suitable career switch found.")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error: Unable to get career switch suggestions from the server.\n{e}")
        return "Error"

def get_work_life_balance(work_hours, stress_level, job_type, vacation_usage):
    """Fetch work-life balance analysis from the backend API."""
    endpoint = f"{BACKEND_URL}/work_life_balance"
    payload = {"work_hours": work_hours, "stress_level": stress_level, "job_type": job_type, "vacation_usage": vacation_usage}
    
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant data
        burnout_risk = data.get("burnout_risk", None)
        work_life_advice = data.get("work_life_balance_advice", "No advice available.")
        
        return burnout_risk if burnout_risk else work_life_advice
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error: Unable to get work-life balance analysis from the server.\n{e}")
        return "Error"

def main():
    st.set_page_config(page_title="AI Career Advisor", page_icon="🚀")
    st.title("🚀 AI Career Advisor")
    
    # Career Advisor Section
    st.header("Career Advisor")
    st.write("Enter your skills and interests below to receive personalized career suggestions.")
    
    with st.form("career_form"):
        user_skills = st.text_input("Your Skills (comma-separated)", placeholder="e.g., Python, Machine Learning, Web Development")
        user_interests = st.text_input("Your Interests (comma-separated)", placeholder="e.g., AI, Cybersecurity, Finance Tech")
        submitted = st.form_submit_button("Get Suggestions")
    
    if submitted:
        if user_skills.strip() and user_interests.strip():
            with st.spinner("🔍 Fetching career suggestions..."):
                suggestions = get_career_suggestions(user_skills, user_interests)
            
            if suggestions:
                st.subheader("🎯 Career Recommendations")
                for idx, suggestion in enumerate(suggestions, start=1):
                    st.write(f"{idx}. {suggestion}")
            else:
                st.warning("🚀 No career suggestions found. Try adjusting your input.")
        else:
            st.warning("⚠️ Please fill out both skills and interests.")
    
    # Career Switch Simulator Section
    st.header("Career Switch Simulator")
    st.write("Simulate a career switch based on your current job, experience, skills, and interests.")
    
    with st.form("career_switch_form"):
        current_job = st.text_input("Current Job", placeholder="e.g., Engineer")
        experience = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)
        skills = st.text_input("Your Skills (comma-separated)", placeholder="e.g., Python, Java")
        interests = st.text_input("Your Interests (comma-separated)", placeholder="e.g., Tech, Education")
        switch_submitted = st.form_submit_button("Simulate Career Switch")
    
    if switch_submitted:
        if current_job.strip() and skills.strip() and interests.strip():
            with st.spinner("🔄 Analyzing best career switch options..."):
                suggested_career = get_career_switch(current_job, experience, skills, interests)
            st.subheader("🔄 Suggested Career Switch")
            st.write(suggested_career)
        else:
            st.warning("⚠️ Please fill out all fields for career switch simulation.")
    
    # Work-Life Balance Analyzer Section
    st.header("Work-Life Balance Analyzer")
    st.write("Analyze your work-life balance and get burnout risk predictions.")
    
    with st.form("work_life_balance_form"):
        work_hours = st.number_input("Work Hours per Week", min_value=0, max_value=168, step=1)
        stress_level = st.slider("Stress Level (1-10)", min_value=1, max_value=10)
        job_type = st.selectbox("Job Type", ["Full-time", "Part-time", "Contract"])
        vacation_usage = st.number_input("Vacation Days Used This Year", min_value=0, max_value=365, step=1)
        balance_submitted = st.form_submit_button("Analyze Work-Life Balance")
    
    if balance_submitted:
        with st.spinner("⚖️ Analyzing work-life balance..."):
            burnout_risk = get_work_life_balance(work_hours, stress_level, job_type, vacation_usage)
        st.subheader("⚖️ Burnout Risk Analysis")
        st.write(f"Burnout Risk Level: {burnout_risk}")

if __name__ == "__main__":
    main()