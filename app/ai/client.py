from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings
def get_llm()->ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
    google_api_key=settings.GEMINI_API,
    model="gemini-3.5-flash-lite",
    temperature=0.7 
)
