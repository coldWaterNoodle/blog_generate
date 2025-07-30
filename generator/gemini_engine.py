import os
import google.generativeai as genai
from google.generativeai import GenerativeModel

# 환경변수에서 API 키 불러오기
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_content(prompt: str) -> str:
    model = GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text
