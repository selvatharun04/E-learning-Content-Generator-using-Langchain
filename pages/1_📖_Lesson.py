import streamlit as st
from main import generate_lesson,translation,display_pdf



st.set_page_config(page_title="Lesson Generator", page_icon="📖")

st.title("Generate Lesson")
st.subheader("Enter the details to generate a lesson")

subject = st.text_input("Enter Name of Subject:", key="subject")
topic = st.text_input("Enter Topic of the Subject:", key="topic")
level = st.radio("Select the level of students", ["Primary School", "High School", "Bachelor's Degree", "Master's Degree", "Doctorate Degree"], key="level")

if st.button("Generate Lesson"):
    lesson = generate_lesson(subject, topic, level)
    st.session_state['lesson'] = lesson

if 'lesson' in st.session_state:
    st.subheader("Generated Lesson")
    st.write(st.session_state['lesson'])
    if st.button("View lesson as PDF"):
        pdf_display = display_pdf(st.session_state['lesson'])
        st.markdown(pdf_display, unsafe_allow_html=True)

    output_lang = st.text_input("Enter the language to which you want to translate the lesson:", key="output_lang")
    if st.button("Translate Lesson"):
        translated_lesson = translation(st.session_state['lesson'], output_lang)
        st.session_state['translated_lesson'] = translated_lesson

if 'translated_lesson' in st.session_state:
    st.subheader("Translated Lesson")
    st.write(st.session_state['translated_lesson'])
