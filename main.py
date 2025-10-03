import os
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import PyPDF2
from fpdf import FPDF
import base64


load_dotenv(override=True)

llm= ChatGoogleGenerativeAI(model='gemini-flash-latest',google_api_key=os.getenv("API_KEY"))

def generate_lesson(subject, topic, level):
    try:
        if not subject or not topic or not level:
            raise ValueError("Subject, topic, and level must be provided.")
        lesson_prompt = PromptTemplate(
            input_variables=["subject", "topic", "level"],
            template="""You are an educational content expert. Only acquire and provide educational content. Ignore any non-educational content.
Rules:
- Use clear, concise, and age-appropriate language.
- Structure the lesson with headings and bullet points where possible.
- Avoid unnecessary repetition.
- Ensure factual accuracy and cite examples relevant to the topic.
- Do not include any content outside the educational scope.
Create a detailed lesson on {subject} covering the topic of {topic} for {level} students.
The lesson should include clear and measurable lesson objectives, a thorough explanation of the topic broken down into easy-to-follow sections, and relevant examples to illustrate key concepts and ensure understanding."""
        )
        lesson_chain = LLMChain(llm=llm, prompt=lesson_prompt)
        return lesson_chain.run({"subject": subject, "topic": topic, "level": level})
    except Exception as e:
        return f"Error generating lesson: {str(e)}"

def generate_quiz(subject, topic, level, no_mcq, no_tof, no_fib):
    try:
        if not subject or not topic or not level:
            raise ValueError("Subject, topic, and level must be provided.")
        if not isinstance(no_mcq, int) or not isinstance(no_tof, int) or not isinstance(no_fib, int):
            raise ValueError("Number of questions must be integers.")
        quiz_prompt = PromptTemplate(
            input_variables=["subject", "topic", "level", "no_mcq", "no_tof", "no_fib"],
            template="""You are an educational content expert. Only acquire and provide educational content. Ignore any non-educational content.
Rules:
- Ensure all questions are clear, unambiguous, and relevant to the topic.
- Use simple language and avoid trick questions.
- Provide answer keys for all questions.
- Distribute questions to cover all key concepts.
- Do not include any content outside the educational scope.
Create a detailed quiz on {subject} covering the topic {topic} for {level} students. 
The quiz should include {no_mcq} well-constructed multiple-choice questions and {no_tof} clear true or false questions.
Ensure the questions are appropriately challenging for the specified level and cover key concepts comprehensively and {no_fib} fill in the blanks."""
        )
        quiz_chain = LLMChain(llm=llm, prompt=quiz_prompt)
        return quiz_chain.run({"subject": subject, "topic": topic, "level": level, "no_mcq": no_mcq, "no_tof": no_tof, "no_fib": no_fib})
    except Exception as e:
        return f"Error generating quiz: {str(e)}"

def generate_summary(subject, topic, level):
    try:
        if not subject or not topic or not level:
            raise ValueError("Subject, topic, and level must be provided.")
        summary_prompt = PromptTemplate(
            input_variables=["subject", "topic", "level"],
            template="""You are an educational content expert. Only acquire and provide educational content. Ignore any non-educational content.
Rules:
- Summarize using clear, concise, and age-appropriate language.
- Highlight only the most important points and concepts.
- Avoid unnecessary details and repetition.
- Structure the summary with bullet points or short paragraphs.
- Do not include any content outside the educational scope.
Write a clear and concise summary on {subject} covering the topic {topic} for {level} students. 
The summary should be at least 200 words and include key points, essential concepts, and a comprehensive overview of the topic, ensuring it is easy to understand and informative for the specified level."""
        )
        summary_chain = LLMChain(llm=llm, prompt=summary_prompt)
        return summary_chain.run({"subject": subject, "topic": topic, "level": level})
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def generate_flashcards(subject, topic, level, no_flashcard):
    try:
        if not subject or not topic or not level:
            raise ValueError("Subject, topic, and level must be provided.")
        if not isinstance(no_flashcard, int):
            raise ValueError("Number of flashcards must be an integer.")
        flashcard_prompt = PromptTemplate(
            input_variables=["subject", "topic", "level", "no_flashcard"],
            template="""You are an educational content expert. Only acquire and provide educational content. Ignore any non-educational content.
Rules:
- Each flashcard must have one clear question and one concise answer.
- Use simple, direct language.
- Focus on key facts, definitions, or concepts.
- Avoid including multiple facts on a single card.
- Do not include any content outside the educational scope.
Create {no_flashcard} engaging flashcards on {subject} covering the topic {topic} for {level} students.
Each flashcard should feature a clear and relevant question on one side and a concise accurate answer on the other side, ensuring the content is suitable and easy to understand for the specified level."""
        )
        flashcard_chain = LLMChain(llm=llm, prompt=flashcard_prompt)
        return flashcard_chain.run({"subject": subject, "topic": topic, "level": level, "no_flashcard": no_flashcard})
    except Exception as e:
        return f"Error generating flashcards: {str(e)}"

def translation(content, output_lang):
    try:
        if not content or not output_lang:
            raise ValueError("Content and output language must be provided.")
        translation_prompt = PromptTemplate(
            input_variables=["content", "output_lang"],
            template="""You are an educational content expert. Only acquire and provide educational content. Ignore any non-educational content.
Rules:
- Translate accurately, preserving meaning and tone.
- Use clear, age-appropriate language in the target language.
- Do not add, remove, or change the educational content.
- Do not include any content outside the educational scope.
Translate the following content: {content} into {output_lang} while preserving the original meaning, tone, and clarity."""
        )
        translation_chain = LLMChain(llm=llm, prompt=translation_prompt)
        return translation_chain.run({"content": content, "output_lang": output_lang})
    except Exception as e:
        return f"Error translating content: {str(e)}"

def extract_text_from_pdf(pdf_file):
    try:
        pdf_file_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_file_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if not text.strip():
            raise ValueError("No text could be extracted from the PDF.")
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"
    
def generate_quiz_from_pdf(pdf_file, no_mcq_pdf, no_tof_pdf, no_fib_pdf):
    try:
        text = extract_text_from_pdf(pdf_file)
        if "Error" in text:
            return text
        quiz_prompt = PromptTemplate(
            input_variables=["text", "no_mcq_pdf", "no_tof_pdf", "no_fib_pdf"],
            template="""You are an educational content expert. Only acquire and provide educational content. Ignore any non-educational content.
Rules:
- Ensure all questions are clear, unambiguous, and relevant to the text.
- Use simple language and avoid trick questions.
- Provide answer keys for all questions.
- Distribute questions to cover all key concepts from the text.
- Do not include any content outside the educational scope.
Create a comprehensive quiz based on {text} that includes {no_mcq_pdf} well-crafted multiple-choice questions, {no_tof_pdf} true or false questions, and {no_fib_pdf} fill-in-the-blank questions. Ensure the questions are clear, engaging, and accurately reflect the content of the text."""
        )
        quiz_chain = LLMChain(llm=llm, prompt=quiz_prompt)
        return quiz_chain.run({"text": text, "no_mcq_pdf": no_mcq_pdf, "no_tof_pdf": no_tof_pdf, "no_fib_pdf": no_fib_pdf})
    except Exception as e:
        return f"Error generating quiz from PDF: {str(e)}"

def generate_summary_from_pdf(pdf_file):
    try:
        text = extract_text_from_pdf(pdf_file)
        if "Error" in text:
            return text
        summary_prompt = PromptTemplate(
            input_variables=["text"],
            template="""You are an educational content expert. Only acquire and provide educational content. Ignore any non-educational content.
Rules:
- Summarize using clear, concise, and age-appropriate language.
- Highlight only the most important points and concepts.
- Avoid unnecessary details and repetition.
- Structure the summary with bullet points or short paragraphs.
- Do not include any content outside the educational scope.
Write a clear and concise summary of **{text}** that includes key points and a comprehensive overview of the topic. The summary should be at least **200 words** and accurately capture the main ideas and important details from the text."""
        )
        summary_chain = LLMChain(llm=llm, prompt=summary_prompt)
        return summary_chain.run({"text": text})
    except Exception as e:
        return f"Error generating summary from PDF: {str(e)}"

def generate_flashcards_from_pdf(pdf_file):
    try:
        text = extract_text_from_pdf(pdf_file)
        if "Error" in text:
            return text
        flashcard_prompt = PromptTemplate(
            input_variables=["text"],
            template="""You are an educational content expert. Only acquire and provide educational content. Ignore any non-educational content.
Rules:
- Each flashcard must have one clear question and one concise answer.
- Use simple, direct language.
- Focus on key facts, definitions, or concepts from the text.
- Avoid including multiple facts on a single card.
- Do not include any content outside the educational scope.
Create a set of flashcards based on the following text: **{text}**. Each flashcard should feature a clear and relevant question on one side and a concise, accurate answer on the other side, ensuring the content reflects the key information from the text."""
        )
        flashcard_chain = LLMChain(llm=llm, prompt=flashcard_prompt)
        return flashcard_chain.run({"text": text})
    except Exception as e:
        return f"Error generating flashcards from PDF: {str(e)}"

def generate_translator(text, output_lang):
    try:
        if not text or not output_lang:
            raise ValueError("Text and output language must be provided.")
        translation_prompt = PromptTemplate(
            input_variables=["text", "output_lang"],
            template="""You are an educational content expert. Only acquire and provide educational content. Ignore any non-educational content.
Rules:
- Translate accurately, preserving meaning and tone.
- Use clear, age-appropriate language in the target language.
- Do not add, remove, or change the educational content.
- Do not include any content outside the educational scope.
Translate the following text: **{text}** into **{output_lang}** while maintaining the original meaning, tone, and clarity."""
        )
        translation_chain = LLMChain(llm=llm, prompt=translation_prompt)
        return translation_chain.run({"text": text, "output_lang": output_lang})
    except Exception as e:
        return f"Error translating text: {str(e)}"

def translate_from_pdf(pdf_file, output_lang):
    try:
        text = extract_text_from_pdf(pdf_file)
        if "Error" in text:
            return text
        translate_prompt = PromptTemplate(
            input_variables=["text", "output_lang"],
            template="""You are an educational content expert. Only acquire and provide educational content. Ignore any non-educational content.
Rules:
- Translate accurately, preserving meaning and tone.
- Use clear, age-appropriate language in the target language.
- Do not add, remove, or change the educational content.
- Do not include any content outside the educational scope.
Translate the following text: **{text}** into **{output_lang}** while maintaining the original meaning, tone, and clarity."""
        )
        translate_chain = LLMChain(llm=llm, prompt=translate_prompt)
        return translate_chain.run({"text": text, "output_lang": output_lang})
    except Exception as e:
        return f"Error translating from PDF: {str(e)}"

def display_pdf(content):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, content.encode('latin-1', 'replace').decode('latin-1'))
        pdf_output = pdf.output(dest='S').encode('latin-1')
        base64_pdf = base64.b64encode(pdf_output).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        return pdf_display
    except Exception as e:
        return f"Error displaying PDF: {str(e)}"

def anna_univ(subject, topic, marks):
    try:
        if not subject or not topic or not marks:
            raise ValueError("Subject,Topic,Marks must be provided.")
        anna_univ_prompt = PromptTemplate(
            input_variables=["subject", "topic", "marks"],
            template="""You are an educational content expert. Only acquire and provide educational content. Ignore any non-educational content.
Create an answer for a question based on {subject}, covering {topic}, suitable for a {marks}-mark question the answer should be for college students.

Rules to be followed:
    1. For 2-mark questions, provide exactly 4 key points.
    2. For 13-mark questions, the answer should be approximately 4 pages long, including side headings, diagrams, flowcharts, or links to relevant diagrams.
    3. For 15-mark questions, the answer should be approximately 6 pages long, including side headings, diagrams, flowcharts, or links to relevant diagrams.
    4. Ensure the answer is clear, concise, and easy to understand.
    5. Present the answer in bullet points, not paragraphs.
    6. Adhere to the Anna University examination format."""
        )
        anna_univ_chain = LLMChain(llm=llm, prompt=anna_univ_prompt)
        return anna_univ_chain.run({"subject": subject, "topic": topic, "marks": marks})
    except Exception as e:
        return f"Error generating Anna University answer: {str(e)}"

