import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
import faiss
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

# Chargez les secrets à partir de Streamlit Cloud
secrets = st.secrets["gemini_api"]

# Accédez à la clé API Gemini
gemini_api_key = secrets["api_key"]

# Configurez l'API Gemini avec la clé API
genai.configure(api_key=gemini_api_key)


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=gemini_api_key)
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)

    # Création de l'index FAISS dans le stockage interne
    index = faiss.create_index(vector_store.get_embedding_dim(), faiss.METRIC_L2)
    index.train(vector_store)
    index.save("/streamlit/static/index.faiss")

    return index


def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details,
    if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="Gemini-pro",
                                   temperature=0.3)

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=gemini_api_key)

    # Chargez l'index FAISS depuis le stockage interne
    try:
        new_db = FAISS.load_local("/streamlit/static/index.faiss", embeddings)
    except RuntimeError as e:
        st.error(e)
    return
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
    {"input_documents": docs, "question": user_question}
  )

    print(response)
    st.write("Reply: ", response["output_text"])

def main():
    st.set_page_config("Chat PDF")
    st.header("Chat pdf développé par Shalom Tehe")

    user_question = st.text_input("Poser une question à partir des fichiers PDF")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Téléchargez vos fichiers PDF et cliquez sur le bouton Soumettre et traiter",
                                     accept_multiple_files=True)
        if st.button("Soumettre et traiter"):
            with st.spinner("Traitement..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Fait")


if __name__ == "__main__":
    main()
