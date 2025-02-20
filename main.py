import os
import streamlit as st 
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import PyPDF2


load_dotenv()

llm= ChatGoogleGenerativeAI(model='gemini-pro',google_api_key=os.getenv("API_KEY"))

def generate_lesson(subject,topic,level):
    lesson_prompt=PromptTemplate(input_variables=[subject,topic,level],
                                 template="Create a lesson on {subject} about {topic} for {level} students that should include Lesson Objectives,Explanation on topic with exaamples")
    lesson_chain= LLMChain(llm=llm,prompt=lesson_prompt)
    return lesson_chain.run({"subject": subject, "topic": topic, "level": level})

def generate_quiz(subject,topic,level):
    quiz_prompt=PromptTemplate(input_variables=[subject,topic,level],
                               template="Create a quiz on {subject} on {topic} for {level} students that should include 5 Multiple Choice Questions,5 true or false questiona and 5 fill in the blanks")
    quiz_chain=LLMChain(llm=llm,prompt=quiz_prompt)
    return quiz_chain.run({"subject": subject, "topic": topic, "level": level})

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

def generate_quiz_from_pdf(pdf_file):
    text=extract_text_from_pdf(pdf_file)
    quiz_prompt=PromptTemplate(input_variables=[text],
                               template="Create a quiz on the {text} that should include 5 Multiple Choice Questions,5 true or false questiona and 5 fill in the blanks")
    quiz_chain=LLMChain(llm=llm,prompt=quiz_prompt)
    return quiz_chain.run({"text": text})

def generate_summary_from_pdf(pdf_file):
    text=extract_text_from_pdf(pdf_file)
    summary_prompt=PromptTemplate(input_variables=[text],
                                  template="Write a summary on the {text} that should include key points,summary of the topic which should be atleast 200 words")
    summary_chain=LLMChain(llm=llm,prompt=summary_prompt)
    return summary_chain.run({"text": text})

st.title("E-Learning Content Generator Using Langchain")
st.header("Enter The Below Details to Generate Lessons , Quiz and Summary")

subject=st.text_input("Enter Name of Subject:")
topic=st.text_input("Enter Topic of the Subject:")
level=st.radio("Select the level of students",["Primary School","High School","Bachelor's Degree","Master's Degree","Doctorate Degree"])

if st.button("Generate Lesson"):
    st.subheader("Generated Lesson")
    st.write(generate_lesson(subject,topic,level))

if st.button("Generate Quiz"):
    st.subheader("Generated Quiz")
    st.write(generate_quiz(subject,topic,level))

if st.button("Generate Summary"):
    st.subheader("Generated Summary")
    st.write(generate_summary(subject,topic,level))
    
pdf_file=st.file_uploader("Upload PDF File",type=['pdf'])
if pdf_file:
    if st.button("Generate Quiz from PDF"):
        st.subheader("Generated Quiz from PDF")
        st.write(generate_quiz_from_pdf(pdf_file))
        
    if st.button("Generate Summary from PDF"):
        st.subheader("Generated Summary from PDF")
        st.write(generate_summary_from_pdf(pdf_file))
        
        



    
         



