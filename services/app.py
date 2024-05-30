import os
import sys
from dotenv import load_dotenv
import streamlit as st
from streamlit_feedback import streamlit_feedback

path_this_file = os.path.dirname(os.path.abspath(__file__))
pat_project_root = os.path.join(path_this_file, "..")
sys.path.append(pat_project_root)

from src.qa_processor import QAProcessor
from src.collection_management import CollectionManagement

class LinkAjaChatbot:
    def __init__(self):
        load_dotenv()
        self.question_temp = ""
        self.answer_temp = ""
        self.coll_man = CollectionManagement()
        self.db = self.coll_man.load_chroma_collection("linkaja")
        self.qa_proc = QAProcessor(self.db)
        self.initialize_ui()
        self.load_chat_history()
    
    def initialize_ui(self):
        st.title("LinkAja Chatbot")
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "Tanyakan hal apapun tentang LinkAja. Kamu bisa bertanya tentang akun, aplikasi, bonus, transaksi, merchant, settlement, dan hal lainnya."}
            ]

    def load_chat_history(self):
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

    def handle_feedback(self):
        st.write(st.session_state.fb_k)
        st.toast("✔️ Feedback diterima!")
        print("question:", self.question_temp, "answer:", self.answer_temp)
        with open('feed_back_log.txt', 'a') as f:
            f.write(f"{st.session_state.fb_k} question: {self.question_temp} answer: {self.answer_temp}\n\n")

    def handle_question(self):
        question = st.chat_input()
        if question:
            st.session_state.messages.append({"role": "user", "content": question})
            st.chat_message("user").write(question)
            content, _ = self.qa_proc.generate_final_answer(question)
            msg = {'role': 'assistant', 'content': content}
            st.session_state.messages.append(msg)
            st.chat_message("assistant").write(msg['content'])
            self.question_temp = question
            self.answer_temp = content
            self.display_feedback_form()

    def display_feedback_form(self):
        with st.form('form'):
            streamlit_feedback(
                feedback_type="thumbs",
                optional_text_label="[Optional] Masukkan penjelasan", 
                align="flex-start", 
                key='fb_k'
            )
            st.form_submit_button('Save feedback', on_click=self.handle_feedback)

if __name__ == "__main__":
    chatbot = LinkAjaChatbot()
    chatbot.handle_question()
