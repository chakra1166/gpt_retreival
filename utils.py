import streamlit as st
from streamlit_chat import message
import chromadb
from typing import Final
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain

DB_DIR: Final = "embeddings/chroma/"

client_settings = chromadb.config.Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=DB_DIR,
    anonymized_telemetry=False,
)


def make_chain(api_key, db_dir=DB_DIR):
    if api_key:
        model = ChatOpenAI(
            model_name="gpt-3.5-turbo", temperature=0.2, openai_api_key=api_key
        )
        embeddings = OpenAIEmbeddings(
            openai_api_key=api_key,
            model="text-embedding-ada-002",
        )
        vectordb = Chroma(
            persist_directory=db_dir,
            embedding_function=embeddings,
            collection_name="capitaland_sustain_report",
            client_settings=client_settings,
        )
        # expose this index in a retriever interface
        retriever = vectordb.as_retriever(
            search_type="similarity", search_kwargs={"k": 10}
        )
        return ConversationalRetrievalChain.from_llm(
            model, retriever=retriever, return_source_documents=True
        )


def get_text(samp_select):
    if samp_select:
        input_text = st.text_input("Query: ", samp_select, key="input")
    else:
        input_text = st.text_input("Query: ", "", key="input")
    return input_text
