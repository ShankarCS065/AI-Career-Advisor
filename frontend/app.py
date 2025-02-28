import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

def main():
    st.title("🚀 AI Career Advisor")
    st.write("Enter your skills and interests below to receive personalized career suggestions.")

    with st.form("career_form"):
        user_skills = st.text_input("Your Skills (comma-separated)", "")
        user_interests = st.text_input("Your Interests (comma-separated)", "")
        submitted = st.form_submit_button("Get Suggestions")

    if submitted:
        if user_skills and user_interests:
            endpoint = f"{BACKEND_URL}/suggest"
            payload = {"skills": user_skills, "interests": user_interests}
            response = requests.post(endpoint, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                st.subheader("Career Recommendations")
                st.write(data["suggestions"])
            else:
                st.error("❌ Error: Unable to get suggestions from the server.")
        else:
            st.warning("⚠️ Please fill out both skills and interests.")

if __name__ == "__main__":
    main()
