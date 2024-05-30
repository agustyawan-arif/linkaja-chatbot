import google.generativeai as genai
from chromadb import Documents, EmbeddingFunction, Embeddings
import os
import sys
from dotenv import load_dotenv

path_this_file = os.path.dirname(os.path.abspath(__file__))
pat_project_root = os.path.join(path_this_file, "..")
sys.path.append(pat_project_root)
load_dotenv()

class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("Gemini API Key not provided. Please provide GEMINI_API_KEY as an environment variable")
        genai.configure(api_key=gemini_api_key)
        model = "models/embedding-001"
        title = "Custom query"
        return genai.embed_content(model=model,
                                   content=input,
                                   task_type="retrieval_document",
                                   title=title)["embedding"]