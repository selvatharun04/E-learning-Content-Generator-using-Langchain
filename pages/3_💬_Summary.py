import streamlit as st
from main import generate_summary, display_pdf,translation

st.set_page_config(page_title="Summary Generator", page_icon="💬")

st.title("Summary Generator")
st.subheader("Enter the Details to Generate Summary")

subject = st.text_input("Enter Name of Subject:", key="subject")
topic = st.text_input("Enter Topic of the Subject:", key="topic")
level = st.radio("Select the level of students", ["Primary School", "High School", "Bachelor's Degree", "Master's Degree", "Doctorate Degree"], key="level")


if st.button("Generate Summary"):
    summary = generate_summary(subject, topic, level)
    st.session_state['summary'] = summary

if 'summary' in st.session_state:
    st.subheader("Summary")
    st.write(st.session_state['summary'])
    
    if st.button("View Summary as PDF"):
        pdf_display = display_pdf(st.session_state['summary'])
        st.markdown(pdf_display, unsafe_allow_html=True)
    
    output_lang = st.text_input("Enter the language to which you want to translate the summary:", key="output_lang")
    if st.button("Translate Summary"):
        translated_summary = translation(st.session_state['summary'], output_lang)
        st.session_state['translated_summary'] = translated_summary

if 'translated_summary' in st.session_state:
    st.subheader("Translated Summary")
    st.write(st.session_state['translated_summary'])