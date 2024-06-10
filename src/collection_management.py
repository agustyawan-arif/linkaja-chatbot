import os
import sys
import srsly
import chromadb
from src.embedding_function import GeminiEmbeddingFunction

path_this_file = os.path.dirname(os.path.abspath(__file__))
pat_project_root = os.path.join(path_this_file, "..")
sys.path.append(pat_project_root)

class CollectionManagement:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path=f"{pat_project_root}/knowledges")
        self.documents = []
        self.metadatas = []
        self.ids = []

    def read_data(self, data_path):
        datas = list(srsly.read_json(data_path))
        for i, data in enumerate(datas):
            self.documents.append(data["question"] + "\n" + data["answer"])
            self.ids.append(str(i))

    def create_collection(self, data_path, collection_name):
        self.read_data(data_path)
        self.collection = self.chroma_client.create_collection(name=collection_name, embedding_function=GeminiEmbeddingFunction())

    def insert_document(self):
        self.collection.add(
            documents = self.documents,
            ids = self.ids
        )

    def load_chroma_collection(self, name):
        db = self.chroma_client.get_collection(name=name, embedding_function=GeminiEmbeddingFunction())
        return db