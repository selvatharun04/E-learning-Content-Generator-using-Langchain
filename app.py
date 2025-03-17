import streamlit as st
from main import generate_lesson, generate_quiz, generate_summary, generate_quiz_from_pdf, generate_summary_from_pdf, translation, translate_from_pdf, save_as_pdf ,generate_flashcards
import base64
from gtts import gTTS

def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def text_to_audio(text, filename):
    tts = gTTS(text)
    tts.save(filename)

def display_audio(file_path):
    audio_file = open(file_path, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3')

st.title("E-Learning Content Generator Using Langchain")
st.header("Enter The Below Details to Generate Lessons , Quiz and Summary")

subject = st.text_input("Enter Name of Subject:", key="subject")
topic = st.text_input("Enter Topic of the Subject:", key="topic")
level = st.radio("Select the level of students", ["Primary School", "High School", "Bachelor's Degree", "Master's Degree", "Doctorate Degree"], key="level")
output_lang = st.text_input("Enter the language to which you want to translate the lesson:", key="output_lang")

no_mcq = st.number_input("Enter Number of Multiple Choice Questions needed for Quiz", min_value=0, max_value=10, key="no_mcq")
no_tof = st.number_input("Enter Number of True or False Questions needed for Quiz", min_value=0, max_value=10, key="no_tof")
no_fib = st.number_input("Enter Number of Fill in the Blanks needed for Quiz", min_value=0, max_value=10, key="no_fib")

if st.button("Generate Lesson"):
    lesson = generate_lesson(subject, topic, level)
    st.subheader("Generated Lesson")
    st.write(lesson)
    st.session_state['lesson'] = lesson

if 'lesson' in st.session_state:
    if st.button("Save Lesson as PDF"):
        save_as_pdf(st.session_state['lesson'], "lesson.pdf")
        st.success("Lesson saved as lesson.pdf")
        display_pdf("lesson.pdf")
    if st.button("Generate Audio Narration for Lesson"):
        text_to_audio(st.session_state['lesson'], "lesson.mp3")
        st.success("Audio narration saved as lesson.mp3")
        display_audio("lesson.mp3")

if st.button("Generate Quiz"):
    quiz = generate_quiz(subject, topic, level, no_mcq, no_tof, no_fib)
    st.subheader("Generated Quiz")
    st.write(quiz)
    st.session_state['quiz'] = quiz

if 'quiz' in st.session_state:
    if st.button("Save Quiz as PDF"):
        save_as_pdf(st.session_state['quiz'], "quiz.pdf")
        st.success("Quiz saved as quiz.pdf")
        display_pdf("quiz.pdf")
    if st.button("Generate Audio Narration for Quiz"):
        text_to_audio(st.session_state['quiz'], "quiz.mp3")
        st.success("Audio narration saved as quiz.mp3")
        display_audio("quiz.mp3")

if st.button("Generate Summary"):
    summary = generate_summary(subject, topic, level)
    st.subheader("Generated Summary")
    st.write(summary)
    st.session_state['summary'] = summary

if 'summary' in st.session_state:
    if st.button("Save Summary as PDF"):
        save_as_pdf(st.session_state['summary'], "summary.pdf")
        st.success("Summary saved as summary.pdf")
        display_pdf("summary.pdf")
    if st.button("Generate Audio Narration for Summary"):
        text_to_audio(st.session_state['summary'], "summary.mp3")
        st.success("Audio narration saved as summary.mp3")
        display_audio("summary.mp3")

if st.button("Generate Flashcards"):
    flashcards = generate_flashcards(subject, topic, level)
    st.subheader("Generated Flashcards")
    st.write(flashcards)
    st.session_state['flashcards'] = flashcards

if 'flashcards' in st.session_state:
    if st.button("Save Flashcards as PDF"):
        save_as_pdf(st.session_state['flashcards'], "flashcards.pdf")
        st.success("Flashcards saved as flashcards.pdf")
        display_pdf("flashcards.pdf")
    if st.button("Generate Audio Narration for Flashcards"):
        text_to_audio(st.session_state['flashcards'], "flashcards.mp3")
        st.success("Audio narration saved as flashcards.mp3")
        display_audio("flashcards.mp3")
    
if st.button("Translate Lesson"):
    translated_lesson = translation(subject, topic, level, output_lang)
    st.subheader("Translated Lesson")
    st.write(translated_lesson)
    st.session_state['translated_lesson'] = translated_lesson

if 'translated_lesson' in st.session_state:
    if st.button("Save Translated Lesson as PDF"):
        save_as_pdf(st.session_state['translated_lesson'], "translated_lesson.pdf")
        st.success("Translated Lesson saved as translated_lesson.pdf")
        display_pdf("translated_lesson.pdf")
    if st.button("Generate Audio Narration for Translated Lesson"):
        text_to_audio(st.session_state['translated_lesson'], "translated_lesson.mp3")
        st.success("Audio narration saved as translated_lesson.mp3")
        display_audio("translated_lesson.mp3")

st.header("Upload PDF File to Generate Quiz and Summary")
pdf_file = st.file_uploader("Upload PDF File", type=['pdf'])
st.subheader("Note: The PDF File should contain text to generate Quiz and Summary after that click on the below buttons to generate Quiz and Summary")

no_mcq_pdf = st.number_input("Enter Number of Multiple Choice Questions needed for Quiz", min_value=0, max_value=10, key="no_mcq_pdf")
no_tof_pdf = st.number_input("Enter Number of True or False Questions needed for Quiz", min_value=0, max_value=10, key="no_tof_pdf")
no_fib_pdf = st.number_input("Enter Number of Fill in the Blanks needed for Quiz", min_value=0, max_value=10, key="no_fib_pdf")
output_lang_pdf = st.text_input("Enter the language to which you want to translate the PDF:", key="output_lang_pdf")

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
            display_pdf("quiz_from_pdf.pdf")
        if st.button("Generate Audio Narration for Quiz from PDF"):
            text_to_audio(st.session_state['quiz_from_pdf'], "quiz_from_pdf.mp3")
            st.success("Audio narration saved as quiz_from_pdf.mp3")
            display_audio("quiz_from_pdf.mp3")

    if st.button("Generate Summary from PDF"):
        summary_from_pdf = generate_summary_from_pdf(pdf_file)
        st.subheader("Generated Summary from PDF")
        st.write(summary_from_pdf)
        st.session_state['summary_from_pdf'] = summary_from_pdf

    if 'summary_from_pdf' in st.session_state:
        if st.button("Save Summary as PDF"):
            save_as_pdf(st.session_state['summary_from_pdf'], "summary_from_pdf.pdf")
            st.success("Summary saved as summary_from_pdf.pdf")
            display_pdf("summary_from_pdf.pdf")
        if st.button("Generate Audio Narration for Summary from PDF"):
            text_to_audio(st.session_state['summary_from_pdf'], "summary_from_pdf.mp3")
            st.success("Audio narration saved as summary_from_pdf.mp3")
            display_audio("summary_from_pdf.mp3")

    if st.button("Translate from PDF"):
        translated_pdf = translate_from_pdf(pdf_file, output_lang_pdf)
        st.subheader("Translated PDF")
        st.write(translated_pdf)
        st.session_state['translated_pdf'] = translated_pdf

    if 'translated_pdf' in st.session_state:
        if st.button("Save Translated PDF as PDF"):
            save_as_pdf(st.session_state['translated_pdf'], "translated_pdf.pdf")
            st.success("Translated PDF saved as translated_pdf.pdf")
            display_pdf("translated_pdf.pdf")
        if st.button("Generate Audio Narration for Translated PDF"):
            text_to_audio(st.session_state['translated_pdf'], "translated_pdf.mp3")
            st.success("Audio narration saved as translated_pdf.mp3")
            display_audio("translated_pdf.mp3")

