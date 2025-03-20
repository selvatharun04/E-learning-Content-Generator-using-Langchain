import streamlit as st
from main import generate_quiz, display_pdf,translation

st.set_page_config(page_title="Quiz Generator", page_icon="📝")

st.title("Quiz Generator")
st.subheader("Enter the below details to generate quiz")

subject = st.text_input("Enter Name of Subject:", key="subject")
topic = st.text_input("Enter Topic of the Subject:", key="topic")
level = st.radio("Select the level of students", ["Primary School", "High School", "Bachelor's Degree", "Master's Degree", "Doctorate Degree"], key="level")

no_mcq = st.number_input("Enter Number of Multiple Choice Questions needed for Quiz", min_value=0, max_value=10, key="no_mcq")
no_tof = st.number_input("Enter Number of True or False Questions needed for Quiz", min_value=0, max_value=10, key="no_tof")
no_fib = st.number_input("Enter Number of Fill in the Blanks needed for Quiz", min_value=0, max_value=10, key="no_fib")

if st.button("Generate Quiz"):
    quiz = generate_quiz(subject, topic, level, no_mcq, no_tof, no_fib)
    st.session_state['quiz'] = quiz

if 'quiz' in st.session_state:
    st.subheader("Generated Quiz")
    st.write(st.session_state['quiz'])

    if st.button("View Quiz as PDF"):
        pdf_display = display_pdf(st.session_state['quiz'])
        st.markdown(pdf_display, unsafe_allow_html=True)
    
    output_lang = st.text_input("Enter the language to which you want to translate the quiz:", key="output_lang")
    if st.button("Translate Quiz"):
        translated_quiz = translation(st.session_state['quiz'], output_lang)
        st.session_state['translated_quiz'] = translated_quiz

if 'translated_quiz' in st.session_state:
    st.subheader("Translated Quiz")
    st.write(st.session_state['translated_quiz'])