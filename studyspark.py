import os
import streamlit as st
from google import genai

# Page configuration
st.set_page_config(page_title="AI Study Assistant", page_icon="📚", layout="wide")

# Initialize Gemini Client
# Make sure GEMINI_API_KEY environment variable is set, or enter it manually below
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    client = genai.Client(api_key=api_key)
else:
    st.warning("Please provide a Gemini API Key to use the app.")
    client = None

# App Title & Subtitle
st.title("📚 AI Powered Study Assistant")
st.write("Enter any topic below to get a custom summary, interactive quiz, and personalized study plan.")

# User Input
topic = st.text_input("Enter a Study Topic / Subject:", placeholder="e.g., Photosynthesis, Quantum Physics, French Revolution")

# Tabs for different features
tab1, tab2, tab3 = st.tabs(["📖 Topic Summary", "❓ Interactive Quiz", "📅 Study Planner"])

if topic and client:
    
    # --- TAB 1: SUMMARY ---
    with tab1:
        st.header(f"Summary: {topic}")
        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                prompt = f"Provide a comprehensive, student-friendly summary of the topic: '{topic}'. Include key concepts, bullet points for easy reading, and simple analogies if applicable."
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt
                )
                st.markdown(response.text)

    # --- TAB 2: QUIZ ---
    with tab2:
        st.header(f"Quiz: {topic}")
        num_questions = st.slider("Select number of questions:", 3, 10, 5)
        
        if st.button("Generate Quiz"):
            with st.spinner("Creating quiz questions..."):
                prompt = f"Generate a {num_questions}-question multiple-choice quiz on the topic '{topic}'. Provide the questions, choices (A, B, C, D), and clearly mark the correct answer at the bottom with brief explanations."
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt
                )
                st.markdown(response.text)

    # --- TAB 3: STUDY PLANNER ---
    with tab3:
        st.header(f"Study Planner: {topic}")
        days = st.number_input("How many days do you have to study this topic?", min_value=1, max_value=30, value=7)
        hours_per_day = st.number_input("Hours available per day:", min_value=0.5, max_value=8.0, value=2.0, step=0.5)
        
        if st.button("Create Study Plan"):
            with st.spinner("Building your custom schedule..."):
                prompt = f"Create a step-by-step study plan to master '{topic}' in {days} days, spending {hours_per_day} hours per day. Break it down day-by-day with specific goals and revision checkpoints."
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt
                )
                st.markdown(response.text)

elif not topic:
    st.info("👆 Please enter a topic above to get started.")