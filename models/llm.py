import os
from keys import google_api
from langchain_openai import ChatOpenAI
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = google_api

gemini_pro = ChatGoogleGenerativeAI(
    model="gemini-pro",
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
)

custom_llm = ChatOpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
