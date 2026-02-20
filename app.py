import streamlit as st
import google.generativeai as genai

# --- 1. SECURE CONFIG ---
st.set_page_config(page_title="SkillLift AI", page_icon="🚀")

def init_ai():
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        return True
    except KeyError:
        st.error("🔑 API Key missing from Secrets.")
        st.stop()

init_ai()

# --- 2. COURSE GENERATOR BRAIN ---
def generate_micro_course(topic):
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    prompt = f"""
    Create a structured 5-day micro-learning course for the topic: '{topic}'.
    For EACH day, provide:
    1. Lesson Title & 3 Key Bullet Points.
    2. A 3-question Multiple Choice Quiz.
    3. A 'Mini-Project' task that increases in difficulty daily.
    
    Structure the response clearly as a 5-day curriculum.
    """
    
    response = model.generate_content(prompt)
    return response.text

# --- 3. UI DASHBOARD ---
st.title("🚀 SkillLift: AI Micro-Course Generator")
topic_input = st.text_input("Enter a skill or topic you want to master:", placeholder="e.g., Prompt Engineering")

if st.button("🏗️ Build My Course"):
    if topic_input:
        with st.status(f"Generating your 5-day journey for {topic_input}...", expanded=True):
            course_content = generate_micro_course(topic_input)
            
        st.subheader("📅 Your Custom 5-Day Curriculum")
        st.markdown(course_content)
        
        # Pro-feature: Export to PDF/Text
        st.download_button("📥 Save Course to Device", course_content, file_name=f"{topic_input}_course.md")
    else:
        st.warning("Please enter a topic first.")
