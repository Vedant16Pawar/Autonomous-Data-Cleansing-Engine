"""
Shared LLM instance for the agent layer.

Every module that needs the LLM should import it from here
instead of instantiating its own ChatGroq client.
"""

import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)
