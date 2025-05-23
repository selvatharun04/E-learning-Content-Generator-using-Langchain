import streamlit as st
from main import generate_translator, extract_text_from_pdf

st.set_page_config(page_title="PDF-Translator", page_icon="🔠")
st.title("PDF Translator")
st.subheader("Upload PDF to Translate")

pdf_file = st.file_uploader("Upload PDF File", type=['pdf'])
output_lang = st.text_input("Enter the language to which you want to translate the PDF:", key="output_lang")

if st.button("Translate PDF"):
    if pdf_file:
        try:
            text = extract_text_from_pdf(pdf_file)
            if not text.strip():
                st.error("The uploaded PDF does not contain any extractable text.")
            else:
                try:
                    translated_pdf = generate_translator(text, output_lang)
                    st.session_state['translated_pdf'] = translated_pdf
                except Exception as e:
                    st.error(f"Error during translation: {e}")
        except Exception as e:
            st.error(f"Error extracting text from PDF: {e}")
    else:
        st.warning("Please upload a valid PDF file.")

if 'translated_pdf' in st.session_state:
    st.subheader("Translated PDF")
    st.write(st.session_state['translated_pdf'])
