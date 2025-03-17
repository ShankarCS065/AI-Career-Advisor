# 🚀 AI Career Advisor  

🌟 **AI Career Advisor** is an intelligent career guidance platform designed to help users navigate their professional journey. Whether you're exploring new career paths, considering a job switch, or analyzing your work-life balance, this AI-powered tool provides **personalized recommendations** to guide your next steps.  

---

## 🚀 Live Demo  
🔗 **Frontend URL:** [https://aicareeradvisor-frontend-production.up.railway.app](#)  
🔗 **Backend URL:** [https://aicareeradvisor-backend-production.up.railway.app](#)  

-----

## 🔥 Why Use AI Career Advisor?  
✅ **AI-Powered Career Suggestions** - Get customized career recommendations based on your skills & interests.  
✅ **Career Switch Simulator** - Find the best career transition opportunities based on your job,experience,skills and interest.  
✅ **Work-Life Balance Analyzer** - Get burnout risk insights and work-life improvement suggestions.  
✅ **Real-Time Insights** - AI-driven insights for smart career decisions.  
✅ **User-Friendly** - A simple and interactive UI built with **Streamlit**.  

----
## 🛠️ Tech Stack  

| **Component**  | **Technology Used**  |
|--------------|---------------------|
| **Frontend** | Streamlit|
| **Backend** | FastAPI,Python,DeepSeekAPI|
| **Database** | PostgreSQL,Redis|
| **Machine Learning** | Scikit-learn (NLP-based Career Recommendation) |
| **Hosting** | Railway.com |
| **tools used** | VSCode,DockerDesktop,Postman|

---

## 📥 Installation & Setup  

### ⚡ **Prerequisites**  
- Python 3.8+
- Virtual Environment (optional but recommended)
- Streamlit & FastAPI installed  

### 🛠 **Step-by-Step Guide**  
```bash
# Clone the repository
git clone https://github.com/yourusername/AI-Career-Advisor.git

# Navigate to the project directory
cd AI-Career-Advisor

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend API
uvicorn backend:app --host 0.0.0.0 --port 8000 --reload

# Run the frontend application
streamlit run frontend.py
