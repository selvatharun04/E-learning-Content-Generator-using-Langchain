import streamlit as st
from main import generate_summary, display_pdf, generate_quiz_from_pdf, generate_summary_from_pdf, generate_flashcards_from_pdf, translation

st.set_page_config(page_title="PDF with AI", page_icon="🎴")

st.title("Generate Flashcards and Summaries from PDF")
st.subheader("Upload PDF to Generate Flashcards, Summaries")

pdf_file = st.file_uploader("Upload PDF File", type=['pdf'])
st.subheader("Note: The PDF File should contain text to generate Flashcard or Summary after that click on the below buttons to generate Quiz and Summary")
col1, col2 = st.columns(2)

with col1:
    button1 = st.button('Generate Flashcards')
with col2:
    button2 = st.button('Generate Summary')

if pdf_file:
    if button1:
        flashcards = generate_flashcards_from_pdf(pdf_file)
        st.subheader("Generated Flashcards")
        st.write(flashcards)
        st.session_state['flashcards'] = flashcards
        
    if st.button("View Flashcards as PDF"):
        pdf_display = display_pdf(st.session_state['flashcards'])
        st.markdown(pdf_display, unsafe_allow_html=True)
   

    if button2:
        summary = generate_summary_from_pdf(pdf_file)
        st.subheader("Generated Summary")
        st.write(summary)
        st.session_state['summary'] = summary
    if st.button("View Summary as PDF"):
        pdf_display = display_pdf(st.session_state['summary'])
        st.markdown(pdf_display, unsafe_allow_html=True)
   

