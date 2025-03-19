import os
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import PyPDF2
from fpdf import FPDF
import base64


load_dotenv(override=True)

llm= ChatGoogleGenerativeAI(model='gemini-1.5-pro',google_api_key=os.getenv("API_KEY"))

def generate_lesson(subject,topic,level):
    lesson_prompt=PromptTemplate(input_variables=[subject,topic,level],
                                 template=""" Create a detailed lesson on {subject} covering the topic of {topic} for {level} students.
                                 The lesson should include Clear and measurable lesson objectives,A thorough explanation of the topic,
                                 broken down into easy-to-follow sections.Relevant examples to illustrate key concepts and ensure understanding """)
    lesson_chain= LLMChain(llm=llm,prompt=lesson_prompt)
    return lesson_chain.run({"subject":subject, "topic":topic, "level": level})

def generate_quiz(subject,topic,level,no_mcq,no_tof,no_fib):
    quiz_prompt=PromptTemplate(input_variables=[subject,topic,level,no_mcq,no_tof,no_fib],
                               template="Create a quiz on {subject} on {topic} for {level} students that should include {no_mcq} Multiple Choice Questions,{no_tof} true or false questions ,"
                               "and {no_fib} fill in the blanks")
    quiz_chain=LLMChain(llm=llm,prompt=quiz_prompt)
    return quiz_chain.run({"subject": subject, "topic": topic, "level": level,"no_mcq": no_mcq ,"no_tof": no_tof,"no_fib": no_fib})

def generate_summary(subject,topic,level):
    summary_prompt=PromptTemplate(input_variables=[subject,topic,level],
                                  template="Write a summary on {subject} on {topic} for {level} students that should include key points,summary of the topic which should be atleast 200 words")
    summary_chain=LLMChain(llm=llm,prompt=summary_prompt)
    return summary_chain.run({"subject": subject, "topic": topic, "level": level})

def generate_flashcards(subject, topic, level,no_flashcard):
    flashcard_prompt = PromptTemplate(input_variables=[subject, topic, level,no_flashcard],
                                      template="Create {no_flashcard} flashcards on {subject} about {topic} for {level} students. Each flashcard should have a question on one side and the answer on the other side.")
    flashcard_chain = LLMChain(llm=llm, prompt=flashcard_prompt)
    return flashcard_chain.run({"subject": subject, "topic": topic, "level": level,"no_flashcard":no_flashcard})

def translation(content,output_lang):
    translation_prompt=PromptTemplate(input_variables=[content,output_lang],
                                     template="Translate the {content} to {output_lang}")
    translation_chain=LLMChain(llm=llm,prompt=translation_prompt)
    return translation_chain.run({"content":content,"output_lang": output_lang})

def extract_text_from_pdf(pdf_file):
    pdf_file_reader=PyPDF2.PdfReader(pdf_file)
    text=" "
    for page in pdf_file_reader.pages:
        text += page.extract_text() + "\n"
    return text

def generate_quiz_from_pdf(pdf_file, no_mcq_pdf, no_tof_pdf, no_fib_pdf):
    text = extract_text_from_pdf(pdf_file)
    quiz_prompt = PromptTemplate(input_variables=[text,no_mcq_pdf,no_tof_pdf,no_fib_pdf],
                                 template="Create a quiz on the {text} that should include {no_mcq_pdf} Multiple Choice Questions, {no_tof_pdf} true or false questions, and {no_fib_pdf} fill in the blanks")
    quiz_chain = LLMChain(llm=llm, prompt=quiz_prompt)
    return quiz_chain.run({"text": text, "no_mcq_pdf": no_mcq_pdf, "no_tof_pdf": no_tof_pdf, "no_fib_pdf": no_fib_pdf})

def generate_summary_from_pdf(pdf_file):
    text=extract_text_from_pdf(pdf_file)
    summary_prompt=PromptTemplate(input_variables=[text],
                                  template="Write a summary on the {text} that should include key points,summary of the topic which should be atleast 200 words")
    summary_chain=LLMChain(llm=llm,prompt=summary_prompt)
    return summary_chain.run({"text": text})

def generate_flashcards_from_pdf(pdf_file):
    text = extract_text_from_pdf(pdf_file)
    flashcard_prompt = PromptTemplate(input_variables=[text],
                                      template="Create flashcards from the following text: {text}. Each flashcard should have a question on one side and the answer on the other side.")
    flashcard_chain = LLMChain(llm=llm, prompt=flashcard_prompt)
    return flashcard_chain.run({"text": text})

def generate_translator(text,output_lang):
    translation_prompt=PromptTemplate(input_variables=[text,output_lang],
                                     template="Translate the {text} to {output_lang} language")
    translation_chain=LLMChain(llm=llm,prompt=translation_prompt)
    return translation_chain.run({"text": text, "output_lang": output_lang})


def translate_from_pdf(pdf_file, output_lang):
    text = extract_text_from_pdf(pdf_file)
    translate_prompt = PromptTemplate(input_variables=[text,output_lang],
                                      template="Translate the {text} to {output_lang} language")
    translate_chain = LLMChain(llm=llm, prompt=translate_prompt)
    return translate_chain.run({"text": text, "output_lang": output_lang})

def display_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content.encode('latin-1', 'replace').decode('latin-1'))
    pdf_output = pdf.output(dest='S').encode('latin-1')
    base64_pdf = base64.b64encode(pdf_output).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    return pdf_display



