import os
from langchain import PromptTemplate
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

from src.collection_management import CollectionManagement

class QAProcessor:
    def __init__(self):
        self.cm = CollectionManagement()
        self.chat_model = ChatGoogleGenerativeAI(model="gemini-pro")
        self.embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.create_prompt()
        self.create_retriever()
        self.create_rag_chain()
    
    def create_prompt(self):
        template = """You are a helpful and informative bot that answers questions using text from the reference context included below. \
            Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
            Your answer must be in Bahasa Indonesia and always answer with friendly tone.\
            If the passage is irrelevant to the answer, you may ignore it.
            QUESTION: '{question}'
            CONTEXT: '{context}'
                
            ANSWER:"""

        self.prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    
    def create_retriever(self):
        langchain_chroma = Chroma(
            client=self.cm.chroma_client,
            collection_name="linkaja",
            embedding_function=self.embedding,
        )

        self.retriever = langchain_chroma.as_retriever(k=3)
    
    def create_rag_chain(self):
        self.rag_chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.chat_model
            | StrOutputParser()
        )
    
    def invoke(self, question):
        return self.rag_chain.invoke(question)