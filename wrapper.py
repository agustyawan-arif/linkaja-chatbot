import os
import sys
import argparse
from dotenv import load_dotenv

path_this_file = os.path.dirname(os.path.abspath(__file__))
pat_project_root = os.path.join(path_this_file, "..")
sys.path.append(pat_project_root)

from src.qa_processor import QAProcessor
from src.collection_management import CollectionManagement

if __name__ == "__main__":
    coll_man = CollectionManagement()
    db = coll_man.load_chroma_collection("linkaja")
    qa_proc = QAProcessor(db)

    args = argparse.ArgumentParser()
    args.add_argument("-q", "--query", default="halo", help="Query/question")
    args = args.parse_args()

    answer, _ = qa_proc.generate_final_answer(args.query)
    print(answer)