import os
import google.generativeai as genai
from src.embedding_function import GeminiEmbeddingFunction
import sys

path_this_file = os.path.dirname(os.path.abspath(__file__))
pat_project_root = os.path.join(path_this_file, "..")
sys.path.append(pat_project_root)

class QAProcessor:
    def __init__(self, db):
        self.db = db

    def make_rag_prompt(self, query, relevant_context):
        escaped = relevant_context.replace("'", "").replace('"', "").replace("\n", " ")
        prompt = ("""You are a helpful and informative bot that answers questions using text from the reference context included below. \
        Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
        Your answer must be in Bahasa Indonesia and always answer with friendly tone.\
        If the passage is irrelevant to the answer, you may ignore it.
        QUESTION: '{query}'
        CONTEXT: '{relevant_context}'
        
        ANSWER:
        """).format(query=query, relevant_context=escaped)
        
        return prompt

    def get_relevant_context(self, query, n_results):
        context = self.db.query(query_texts=[query], n_results=n_results)#['documents'][0]
        return context
        
    def generate_answer(self, prompt):
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-pro')
        answer = model.generate_content(prompt)
        return answer.text

    def generate_final_answer(self, query):
        relevant_info = self.get_relevant_context(query, n_results=3)
        relevant_text = relevant_info["documents"][0]
        relevant_context = "\n".join(x["answer"] for x in relevant_info["metadatas"][0])
        prompt = self.make_rag_prompt(query,relevant_context=relevant_context)
        answer = self.generate_answer(prompt)
        
        return answer, relevant_info