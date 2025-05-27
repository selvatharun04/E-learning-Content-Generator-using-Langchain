import streamlit as st
from main import (
    llm,  # Import the llm object
    generate_lesson,
    generate_quiz,
    generate_summary,
    generate_flashcards,
    translation,
    generate_quiz_from_pdf,
    generate_summary_from_pdf,
    generate_flashcards_from_pdf,
    translate_from_pdf,
    anna_univ
)

# Define the available services and their required fields
SERVICE_FIELDS = {
    "Generate Lesson": ["subject", "topic", "level"],
    "Generate Quiz": ["subject", "topic", "level", "no_mcq", "no_tof", "no_fib"],
    "Generate Summary": ["subject", "topic", "level"],
    "Generate Flashcards": ["subject", "topic", "level", "no_flashcard"],
    "Translate Text": ["content", "output_lang"],
    "Generate Quiz from PDF": ["pdf_file", "no_mcq_pdf", "no_tof_pdf", "no_fib_pdf"],
    "Generate Summary from PDF": ["pdf_file"],
    "Generate Flashcards from PDF": ["pdf_file"],
    "Translate from PDF": ["pdf_file", "output_lang"],
    "Generate Anna University Answer": ["subject", "topic", "marks"]
}

# Initialize Streamlit session state variables
st.title("E-Learning Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "service" not in st.session_state:
    st.session_state.service = None
if "service_confirmed" not in st.session_state:
    st.session_state.service_confirmed = False
if "inputs" not in st.session_state:
    st.session_state.inputs = {}
if "awaiting_field" not in st.session_state:
    st.session_state.awaiting_field = None

# Function to process the selected service
def process_service(service, inputs):
    try:
        if service == "Generate Lesson":
            return generate_lesson(inputs["subject"], inputs["topic"], inputs["level"])
        elif service == "Generate Quiz":
            return generate_quiz(inputs["subject"], inputs["topic"], inputs["level"], int(inputs["no_mcq"]), int(inputs["no_tof"]), int(inputs["no_fib"]))
        elif service == "Generate Summary":
            return generate_summary(inputs["subject"], inputs["topic"], inputs["level"])
        elif service == "Generate Flashcards":
            return generate_flashcards(inputs["subject"], inputs["topic"], inputs["level"], int(inputs["no_flashcard"]))
        elif service == "Translate Text":
            return translation(inputs["content"], inputs["output_lang"])
        elif service == "Generate Quiz from PDF":
            return generate_quiz_from_pdf(inputs["pdf_file"], int(inputs["no_mcq_pdf"]), int(inputs["no_tof_pdf"]), int(inputs["no_fib_pdf"]))
        elif service == "Generate Summary from PDF":
            return generate_summary_from_pdf(inputs["pdf_file"])
        elif service == "Generate Flashcards from PDF":
            return generate_flashcards_from_pdf(inputs["pdf_file"])
        elif service == "Translate from PDF":
            return translate_from_pdf(inputs["pdf_file"], inputs["output_lang"])
        elif service == "Generate Anna University Answer":
            return anna_univ(inputs["subject"], inputs["topic"], int(inputs["marks"]))
        else:
            return "Unknown service."
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Function to handle general queries using llm
def handle_general_query(query):
    try:
        response = llm.predict(query)
        return response
    except Exception as e:
        return f"Error processing query: {str(e)}"

# Display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Reset button to clear the chat and state
if st.button("Reset Chat"):
    st.session_state.chat_history = []
    st.session_state.service = None
    st.session_state.service_confirmed = False
    st.session_state.inputs = {}
    st.session_state.awaiting_field = None

# Service selection and confirmation
if not st.session_state.service_confirmed:
    service = st.selectbox("Select a service", list(SERVICE_FIELDS.keys()), key="service_select")
    if st.button("Start", key="start_btn"):
        st.session_state.service = service
        st.session_state.inputs = {}
        st.session_state.awaiting_field = SERVICE_FIELDS[service][0]
        st.session_state.service_confirmed = True
        st.session_state.chat_history.append({"role": "assistant", "content": f"You selected **{service}**. Let's get started!\nPlease provide {st.session_state.awaiting_field.replace('_', ' ')}:"})

# Main chat input logic (only after service is confirmed)
elif st.session_state.service_confirmed and st.session_state.service:
    fields = SERVICE_FIELDS[st.session_state.service]
    next_field = st.session_state.awaiting_field

    # Handle file upload for PDF fields
    if next_field == "pdf_file":
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], key=f"pdf_{st.session_state.service}", help="Upload a PDF file")
        if uploaded_file and next_field not in st.session_state.inputs:
            st.session_state.inputs[next_field] = uploaded_file
            st.session_state.chat_history.append({"role": "assistant", "content": "PDF received."})
            idx = fields.index(next_field)
            if idx + 1 < len(fields):
                st.session_state.awaiting_field = fields[idx + 1]
                st.session_state.chat_history.append({"role": "assistant", "content": f"Please provide {fields[idx+1].replace('_', ' ')}:"})
            else:
                st.session_state.chat_history.append({"role": "assistant", "content": "_Thinking..._"})
                with st.spinner("Generating response..."):
                    result = process_service(st.session_state.service, st.session_state.inputs)
                if result:
                    st.session_state.chat_history[-1] = {"role": "assistant", "content": str(result)}
                else:
                    st.session_state.chat_history[-1] = {"role": "assistant", "content": "Failed to generate response."}
                # Reset for next conversation
                st.session_state.service = None
                st.session_state.service_confirmed = False
                st.session_state.inputs = {}
                st.session_state.awaiting_field = None

    # Handle text or numeric input fields
    else:
        user_input = st.chat_input(f"Type your {next_field.replace('_', ' ')}...", key=f"chat_{next_field}")
        if user_input and next_field not in st.session_state.inputs:
            # Input validation for numeric fields
            if next_field in ["no_mcq", "no_tof", "no_fib", "no_flashcard", "no_mcq_pdf", "no_tof_pdf", "no_fib_pdf", "marks"]:
                try:
                    value = int(user_input)
                    if value <= 0:
                        st.session_state.chat_history.append({"role": "assistant", "content": "Please enter a positive number."})
                        
                    st.session_state.inputs[next_field] = value
                except ValueError:
                    st.session_state.chat_history.append({"role": "assistant", "content": "Please enter a valid number."})
                    
            else:
                st.session_state.inputs[next_field] = user_input

            st.session_state.chat_history.append({"role": "user", "content": user_input})
            idx = fields.index(next_field)
            if idx + 1 < len(fields):
                st.session_state.awaiting_field = fields[idx + 1]
                st.session_state.chat_history.append({"role": "assistant", "content": f"Please provide {fields[idx+1].replace('_', ' ')}:"})
            else:
                st.session_state.chat_history.append({"role": "assistant", "content": "_Thinking..._"})
                with st.spinner("Generating response..."):
                    result = process_service(st.session_state.service, st.session_state.inputs)
                if result:
                    st.session_state.chat_history[-1] = {"role": "assistant", "content": str(result)}
                else:
                    st.session_state.chat_history[-1] = {"role": "assistant", "content": "Failed to generate response."}
                # Reset for next conversation
                st.session_state.service = None
                st.session_state.service_confirmed = False
                st.session_state.inputs = {}
                st.session_state.awaiting_field = None

# Handle general queries outside of service-specific logic
else:
    user_query = st.chat_input("Ask me anything...")
    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.spinner("Thinking..."):
            response = handle_general_query(user_query)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
