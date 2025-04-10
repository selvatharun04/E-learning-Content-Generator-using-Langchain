import streamlit as st
from main import generate_flashcards, display_pdf, translation

st.set_page_config(page_title="Flashcard Generator", page_icon="🗒️")

st.title("Flashcard Generator")
st.subheader("Enter the Details to Generate Flashcards")

subject = st.text_input("Enter Name of Subject:", key="subject")
topic = st.text_input("Enter Topic of the Subject:", key="topic")
level = st.radio("Select the level of students", ["Primary School", "High School", "Bachelor's Degree", "Master's Degree", "Doctorate Degree"], key="level")
no_flashcard = st.number_input("Number of Flashcards to be Generated", min_value=0, max_value=10, key="no_flashcard")

if st.button("Generate Flashcards"):
    try:
        flashcards = generate_flashcards(subject, topic, level, no_flashcard)
        st.session_state['flashcards'] = flashcards
    except Exception as e:
        st.error(f"An error occurred while generating the flashcards: {e}")

if 'flashcards' in st.session_state:
    st.subheader("Generated Flashcards")
    st.write(st.session_state['flashcards'])

    if st.button("View Flashcards as PDF"):
        try:
            pdf_display = display_pdf(st.session_state['flashcards'])
            st.markdown(pdf_display, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An error occurred while generating the PDF: {e}")
    
    output_lang = st.text_input("Enter the language to which you want to translate the flashcards:", key="output_lang")
    if st.button("Translate Flashcards"):
        try:
            translated_flashcards = translation(st.session_state['flashcards'], output_lang)
            st.session_state['translated_flashcards'] = translated_flashcards
        except Exception as e:
            st.error(f"An error occurred while translating the flashcards: {e}")

if 'translated_flashcards' in st.session_state:
    st.subheader("Translated Flashcards")
    st.write(st.session_state['translated_flashcards'])
