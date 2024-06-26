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
        self.chroma_client = chromadb.PersistentClient(path="knowledges")
        self.documents = []
        self.metadatas = []
        self.ids = []

    def read_data(self, data_path):
        datas = list(srsly.read_json(data_path))
        for i, data in enumerate(datas):
            self.documents.append(data["question"])
            topik = data["topik"] if "topic" in data.keys() else ""
            level = data["level"] if "level" in data.keys() else ""
            self.metadatas.append(
                {
                    "answer": data["answer"],
                    "topik": topik,
                    "level": level
                }
            )
            self.ids.append(str(i))

    def create_collection(self, data_path, collection_name):
        self.read_data(data_path)
        self.collection = self.chroma_client.create_collection(name=collection_name, embedding_function=GeminiEmbeddingFunction())

    def insert_document(self):
        self.collection.add(
            documents = self.documents,
            metadatas = self.metadatas,
            ids = self.ids
        )

    def load_chroma_collection(self, name):
        chroma_client = chromadb.PersistentClient(path="knowledges")
        db = self.chroma_client.get_collection(name=name, embedding_function=GeminiEmbeddingFunction())
        return db