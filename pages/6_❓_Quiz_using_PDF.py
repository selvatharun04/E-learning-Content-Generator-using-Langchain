import streamlit as st
from main import generate_quiz_from_pdf, display_pdf, translation

st.set_page_config(page_title="Quiz using PDF", page_icon="❓")
st.title("Generate Quiz from PDF")
st.subheader("Upload PDF to Generate Quiz")

pdf_file = st.file_uploader("Upload PDF File", type=['pdf'])
no_mcq_pdf = st.number_input("Enter Number of Multiple Choice Questions needed for Quiz", min_value=0, max_value=10, key="no_mcq_pdf")
no_tof_pdf = st.number_input("Enter Number of True or False Questions needed for Quiz", min_value=0, max_value=10, key="no_tof_pdf")
no_fib_pdf = st.number_input("Enter Number of Fill in the Blanks needed for Quiz", min_value=0, max_value=10, key="no_fib_pdf")

if pdf_file:
    if st.button("Generate Quiz"):
        quiz = generate_quiz_from_pdf(pdf_file,no_mcq_pdf, no_tof_pdf, no_fib_pdf)
        st.subheader("Generated Quiz")
        st.write(quiz)
        st.session_state['quiz'] = quiz
    if st.button("View Quiz as PDF"):
        pdf_display = display_pdf(st.session_state['quiz'])
        st.markdown(pdf_display, unsafe_allow_html=True)
    output_lang = st.text_input("Enter the language to which you want to translate the quiz:", key="output_lang")
    if st.button("Translate Quiz"):
        translated_quiz = translation(st.session_state['quiz'], output_lang)
        st.subheader("Translated Quiz")
        st.write(translated_quiz)