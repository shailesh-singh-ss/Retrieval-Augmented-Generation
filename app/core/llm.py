import google.generativeai as genai
from app.core.config import settings
from typing import List, Dict

class GeminiLLM:
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)

    def generate_response(self, prompt: str, context: List[str]) -> str:
        try:
            full_prompt = f"""
            You are a knowledgeable assistant. Use ONLY the following context to answer the question.

            Context:
            {context}

            Question:
            {prompt}

            Answer Guidelines:
            - Provide a concise, accurate answer (1–2 sentences).
            - If the answer is not found in the context, reply: "I don't know based on the provided documents."
            - Briefly explain your reasoning in a short list of key points.
            """
            
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Failed to generate response: {str(e)}")