import os
import streamlit as st 
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import PyPDF2
from fpdf import FPDF

load_dotenv()

llm= ChatGoogleGenerativeAI(model='gemini-pro',google_api_key=os.getenv("API_KEY"))

def generate_lesson(subject,topic,level):
    lesson_prompt=PromptTemplate(input_variables=[subject,topic,level],
                                 template="Create a lesson on {subject} about {topic} for {level} students that should include Lesson Objectives,Explanation on topic with examples")
    lesson_chain= LLMChain(llm=llm,prompt=lesson_prompt)
    return lesson_chain.run({"subject": subject, "topic": topic, "level": level})

def generate_quiz(subject,topic,level,no_mcq,no_tof,no_fib):
    quiz_prompt=PromptTemplate(input_variables=[subject,topic,level,no_mcq,no_tof,no_fib],
                               template="Create a quiz on {subject} on {topic} for {level} students that should include {no_mcq} Multiple Choice Questions,{no_tof} true or false questions and {no_fib} fill in the blanks")
    quiz_chain=LLMChain(llm=llm,prompt=quiz_prompt)
    return quiz_chain.run({"subject": subject, "topic": topic, "level": level,"no_mcq": no_mcq ,"no_tof": no_tof,"no_fib": no_fib})

def generate_summary(subject,topic,level):
    summary_prompt=PromptTemplate(input_variables=[subject,topic,level],
                                  template="Write a summary on {subject} on {topic} for {level} students that should include key points,summary of the topic which should be atleast 200 words")
    summary_chain=LLMChain(llm=llm,prompt=summary_prompt)
    return summary_chain.run({"subject": subject, "topic": topic, "level": level})


def extract_text_from_pdf(pdf_file):
    pdf_file_reader=PyPDF2.PdfReader(pdf_file)
    text=" "
    for page in pdf_file_reader.pages:
        text += page.extract_text() + "\n"
    return text

def generate_quiz_from_pdf(pdf_file,no_mcq_pdf,no_tof_pdf,no_fib_pdf):
    text=extract_text_from_pdf(pdf_file)
    quiz_prompt=PromptTemplate(input_variables=[text,no_mcq_pdf,no_tof_pdf,no_fib_pdf],
                               template="Create a quiz on the {text} that should include {no_mcq_pdf} Multiple Choice Questions,{no_tof_pdf} true or false questiona and {no_fib_pdf} fill in the blanks")
    quiz_chain=LLMChain(llm=llm,prompt=quiz_prompt)
    return quiz_chain.run({"text": text})

def generate_summary_from_pdf(pdf_file):
    text=extract_text_from_pdf(pdf_file)
    summary_prompt=PromptTemplate(input_variables=[text],
                                  template="Write a summary on the {text} that should include key points,summary of the topic which should be atleast 200 words")
    summary_chain=LLMChain(llm=llm,prompt=summary_prompt)
    return summary_chain.run({"text": text})


def save_as_pdf(content, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(filename)

st.title("E-Learning Content Generator Using Langchain")
st.header("Enter The Below Details to Generate Lessons , Quiz and Summary")

subject=st.text_input("Enter Name of Subject:")
topic=st.text_input("Enter Topic of the Subject:")
level=st.radio("Select the level of students",["Primary School","High School","Bachelor's Degree","Master's Degree","Doctorate Degree"])

no_mcq=st.number_input("Enter Number of Multiple Choice Questions needed for Quiz",min_value=0,max_value=10,key="no_mcq")
no_tof=st.number_input("Enter Number of True or False Questions needed for Quiz",min_value=0,max_value=10,key="no_tof")
no_fib=st.number_input("Enter Number of Fill in the Blanks needed for Quiz",min_value=0,max_value=10,key="no_fib")

if st.button("Generate Lesson"):
    lesson = generate_lesson(subject, topic, level)
    st.subheader("Generated Lesson")
    st.write(lesson)
    st.session_state['lesson'] = lesson

if 'lesson' in st.session_state:
    if st.button("Save Lesson as PDF"):
        save_as_pdf(st.session_state['lesson'], "lesson.pdf")
        st.success("Lesson saved as lesson.pdf")

if st.button("Generate Quiz"):
    quiz = generate_quiz(subject, topic, level, no_mcq, no_tof, no_fib)
    st.subheader("Generated Quiz")
    st.write(quiz)
    st.session_state['quiz'] = quiz

if 'quiz' in st.session_state:
    if st.button("Save Quiz as PDF"):
        save_as_pdf(st.session_state['quiz'], "quiz.pdf")
        st.success("Quiz saved as quiz.pdf")

if st.button("Generate Summary"):
    summary = generate_summary(subject, topic, level)
    st.subheader("Generated Summary")
    st.write(summary)
    st.session_state['summary'] = summary

if 'summary' in st.session_state:
    if st.button("Save Summary as PDF"):
        save_as_pdf(st.session_state['summary'], "summary.pdf")
        st.success("Summary saved as summary.pdf")
    
st.header("Upload PDF File to Generate Quiz and Summary")
pdf_file=st.file_uploader("Upload PDF File",type=['pdf'])
st.subheader("Note: The PDF File should contain text to generate Quiz and Summary after that click on the below buttons to generate Quiz and Summary")

no_mcq_pdf=st.number_input("Enter Number of Multiple Choice Questions needed for Quiz",min_value=0,max_value=10,key="no_mcq_pdf")
no_tof_pdf=st.number_input("Enter Number of True or False Questions needed for Quiz",min_value=0,max_value=10,key="no_tof_pdf")
no_fib_pdf=st.number_input("Enter Number of Fill in the Blanks needed for Quiz",min_value=0,max_value=10,key="no_fib_pdf")

if pdf_file:
    if st.button("Generate Quiz from PDF"):
        quiz_from_pdf = generate_quiz_from_pdf(pdf_file, no_mcq_pdf, no_tof_pdf, no_fib_pdf)
        st.subheader("Generated Quiz from PDF")
        st.write(quiz_from_pdf)
        st.session_state['quiz_from_pdf'] = quiz_from_pdf
        
    if 'quiz_from_pdf' in st.session_state:
        if st.button("Save Quiz from PDF as PDF"):
            save_as_pdf(st.session_state['quiz_from_pdf'], "quiz_from_pdf.pdf")
            st.success("Quiz saved as quiz_from_pdf.pdf")
        
    if st.button("Generate Summary from PDF"):
        summary_from_pdf = generate_summary_from_pdf(pdf_file)
        st.subheader("Generated Summary from PDF")
        st.write(summary_from_pdf)
        st.session_state['summary_from_pdf'] = summary_from_pdf

    if 'summary_from_pdf' in st.session_state:
        if st.button("Save Summary as PDF"):
            save_as_pdf(st.session_state['summary_from_pdf'], "summary_from_pdf.pdf")
            st.success("Summary saved as summary_from_pdf.pdf")













