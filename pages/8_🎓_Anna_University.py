import streamlit as st 
from main import anna_univ,display_pdf

st.set_page_config(page_title="Anna University", page_icon="🎓")
st.title("Anna University Question Answer Generator for Students")

st.subheader("Enter the details to generate answer")
subject = st.text_input("Enter Name of Subject:", key="subject")
topic = st.text_input("Enter Topic of the Subject:", key="topic")
marks = st.radio("Select the marks of the question", ["2 Marks", "13 Marks", "15 Marks"], key="marks")

if st.button("Generate Answer"):
    try:
        answer = anna_univ(subject, topic, marks)
        if "Error" in answer:
            st.error(answer)
        else:
            st.session_state['answer'] = answer
    except Exception as e:
        st.error(f"An error occurred while generating the answer: {str(e)}")
        
if 'answer' in st.session_state:
    st.subheader("Generated Answer")
    st.write(st.session_state['answer'])
    if st.button("View answer as PDF"):
        try:
            pdf_display = display_pdf(st.session_state['answer'])
            st.markdown(pdf_display, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An error occurred while displaying the answer as PDF: {str(e)}")