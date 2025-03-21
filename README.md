# E-Learning Content Generator using Langchain and Streamlit

This Project is an E-learning content generator that uses langchain and streamlit that can generate lessons,quizzes,summary,flashcard and translations

I also include some additional features For Uploading PDF file to generate quizzes,summaries,flashcard and translation of the PDF

# Features that are available:

- Generate detailed lessons based on subjects, topic, level of the student
- Generate Quizzes based on subject, topic, level of the student and the user can include how many number of Multi-Choice Questions,True or Flase and Fill in the Blanks to be added
- Generate Summaries based on Subject,Topic, and Level of the Students
- Translate Lesson,Quizes and Summaries into our desired language
- Can able to download the generated lesson,quiz,summaries into PDF
- Upload PDF files to generate summaries,quizzes,and translations for the PDF

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/e-learning-content-generator.git
   cd e-learning-content-generator

2. Create a virtual enviroment and activate it:
    ```sh
    python -m venv .venv
    .venv\Scripts\activate

3. Install the required dependencies:
    ```sh 
    pip install -r requirements.txt

4. Set up environment variables: Create a .env file in the root directory   and add your Google API key:
    ```sh
    API_KEY=your_google_api_key

5. Run Home.py to run the streamlit application
    ```sh
    streamlit run Home.py

# Page Overview

1. File : main.py
    
    Description : This file contains the core functions for generating lessons, quizzes, summaries, translations, and flashcards. It also includes functions for extracting text from PDF files and generating content from PDFs.

- Function: generate_lesson

        Purpose: Generates a detailed lesson based on the subject, topic, and level of the students.
        Parameters: subject, topic, level
        Returns: A generated lesson as a string.
- Function: generate_quiz

        Purpose: Generates a quiz based on the subject, topic, level, and the number of different types of questions.
        Parameters: subject, topic, level, no_mcq, no_tof, no_fib
        Returns: A generated quiz as a string.
- Function: generate_summary

        Purpose: Generates a summary based on the subject, topic, and level of the students.
        Parameters: subject, topic, level
        Returns: A generated summary as a string.
- Function: generate_flashcards

        Purpose: Generates flashcards based on the subject, topic, level, and the number of flashcards.
        Parameters: subject, topic, level, no_flashcard
        Returns: Generated flashcards as a string.
- Function: translation

        Purpose: Translates the given content into the specified language.
        Parameters: content, output_lang
        Returns: Translated content as a string.
- Function: extract_text_from_pdf

        Purpose: Extracts text from a PDF file.
        Parameters: pdf_file
        Returns: Extracted text as a string.

- Function: generate_quiz_from_pdf

        Purpose: Generates a quiz from the content of a PDF file.
        Parameters: pdf_file, no_mcq_pdf, no_tof_pdf, no_fib_pdf
        Returns: Generated quiz as a string.

- Function: generate_summary_from_pdf

        Purpose: Generates a summary from the content of a PDF file.
        Parameters: pdf_file
        Returns: Generated summary as a string.

- Function: generate_flashcards_from_pdf

        Purpose: Generates flashcards from the content of a PDF file.
        Parameters: pdf_file
        Returns: Generated flashcards as a string.

- Function: generate_translator

        Purpose: Translates the given text into the specified language.
        Parameters: text, output_lang
        Returns: Translated text as a string.

- Function: translate_from_pdf

        Purpose: Translates the content of a PDF file into the specified language.
        Parameters: pdf_file, output_lang
        Returns: Translated content as a string.

- Function: display_pdf

        Purpose: Converts the given content into a PDF and returns an HTML iframe to display the PDF.
        Parameters: content
        Returns: HTML iframe to display the PDF.

2. File : Home.py
    
    Description : This is the main entry point of the Streamlit application. It provides an overview of the project and links to other pages for generating lessons, quizzes, summaries, translations, and handling PDF uploads.

3. File : pages/1_📚_Lesson_Generator.py
    
    Description :  Generate detailed lessons based on the subject, topic, level of the students. Users can input the required details and generate a lesson, which can then be viewed and downloaded as a PDF.

4. File : pages/2_📝_Quiz_Generator.py
    
    Description : Generate quizzes based on the subject, topic, level of the students, and the number of multiple-choice questions, true/false questions, and fill-in-the-blank questions. Users can input the required details and generate a quiz, which can then be viewed and downloaded as a PDF.

5. File : pages/3_💬_Summary.py
    
    Description : Generate summaries based on the subject, topic, and level of the students. Users can input the required details and generate a summary, which can then be viewed and downloaded as a PDF. Additionally, users can translate the summary into different languages.

6. File : pages/4_📇_Flashcard_Generator.py
    
    Description : Generate flashcards based on the subject, topic, level of the students, and the number of flashcards. Users can input the required details and generate flashcards, which can then be viewed and downloaded as a PDF.

7. File : pages/5_🎴_PDF_Extractor.py
    
    Description : Upload a PDF file and generate summary and flashcard from its content. which can be viewed as a PDF

8. File : 6_❓_Quiz_using_PDF.py

    Description : Upload a PDF file and generate quizzes from its content. Users can specify the number of multiple-choice questions, true/false questions, and fill-in-the-blank questions to be generated from the PDF content.

9. File : pages/7_🔠_Translator.py
    
    Description : Upload a PDF file and translate its content into a different language. Users can specify the target language and translate the PDF content, which can then be viewed and downloaded as a PDF