import streamlit as st
from main import generate_lesson, translation, display_pdf

st.set_page_config(page_title="Lesson Generator", page_icon="📖")

st.title("Generate Lesson")
st.subheader("Enter the details to generate a lesson")

subject = st.text_input("Enter Name of Subject:", key="subject")
topic = st.text_input("Enter Topic of the Subject:", key="topic")
level = st.radio("Select the level of students", ["Primary School", "High School", "Bachelor's Degree", "Master's Degree", "Doctorate Degree"], key="level")

if st.button("Generate Lesson"):
    try:
        lesson = generate_lesson(subject, topic, level)
        if "Error" in lesson:
            st.error(lesson)
        else:
            st.session_state['lesson'] = lesson
    except Exception as e:
        st.error(f"An error occurred while generating the lesson: {str(e)}")

if 'lesson' in st.session_state:
    st.subheader("Generated Lesson")
    st.write(st.session_state['lesson'])
    if st.button("View lesson as PDF"):
        try:
            pdf_display = display_pdf(st.session_state['lesson'])
            st.markdown(pdf_display, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An error occurred while displaying the lesson as PDF: {str(e)}")

    output_lang = st.text_input("Enter the language to which you want to translate the lesson:", key="output_lang")
    if st.button("Translate Lesson"):
        try:
            translated_lesson = translation(st.session_state['lesson'], output_lang)
            if "Error" in translated_lesson:
                st.error(translated_lesson)
            else:
                st.session_state['translated_lesson'] = translated_lesson
        except Exception as e:
            st.error(f"An error occurred while translating the lesson: {str(e)}")

if 'translated_lesson' in st.session_state:
    st.subheader("Translated Lesson")
    st.write(st.session_state['translated_lesson'])
