from langchain_google_genai import ChatGoogleGenerativeAI 
from dotenv import load_dotenv
from langgraph.graph import START,MessagesState,StateGraph
from langchain_core.messages import HumanMessage
import os 
load_dotenv(override=True)

llm= ChatGoogleGenerativeAI(model='gemini-1.5-pro',google_api_key=os.getenv("API_KEY"))

