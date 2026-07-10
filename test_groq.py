import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

# Load environment variables from .env
load_dotenv()

# Create the Groq LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
)

response = llm.invoke(
    [
        HumanMessage(
            content="Hello! Tell me one interesting fact about pandas."
        )
    ]
)

print("\nResponse:\n")
print(response.content)