import streamlit as st
import requests

# Use "backend" instead of "localhost" when running in Docker
BACKEND_URL = "http://backend:8000"

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

            try:
                response = requests.post(endpoint, json=payload)
                response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)

                data = response.json()
                st.subheader("Career Recommendations")
                st.write(data.get("suggestions", "No suggestions available."))

            except requests.exceptions.RequestException as e:
                st.error(f"❌ Error: Unable to get suggestions from the server.\n{e}")
        else:
            st.warning("⚠️ Please fill out both skills and interests.")

if __name__ == "__main__":
    main()
