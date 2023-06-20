import streamlit as st
from streamlit_chat import message
import chromadb
from typing import Final
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
import os
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from conf.questions import sample_q

DB_DIR: Final = "embeddings/chroma/"

client_settings = chromadb.config.Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=DB_DIR,
    anonymized_telemetry=False,
)

with st.sidebar:
    api_key = st.text_input(label="Enter Open AI API Key")


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
            collection_name="Yonsin_Annual_Report_2023_1-25_pages",
            client_settings=client_settings,
        )
        # expose this index in a retriever interface
        retriever = vectordb.as_retriever(
            search_type="similarity", search_kwargs={"k": 5}
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


# From here down is all the StreamLit UI.
st.header("Yinson Annual Report Chat Demo")
chat_chain = make_chain(api_key=api_key, db_dir=DB_DIR)
samp_select = st.selectbox(label="Select sample questions", options=sample_q)

# initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content="You are a helpful assistant.")]

user_input = get_text(samp_select=samp_select)
if user_input and api_key:
    st.session_state.messages.append(HumanMessage(content=user_input))
    with st.spinner("Thinking..."):
        response = chat_chain({"question": user_input, "chat_history": []})
    st.session_state.messages.append(AIMessage(content=response["answer"]))

    # display message history
    messages = st.session_state.get("messages", [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + "_user")
        else:
            message(msg.content, is_user=False, key=str(i) + "_ai")

    # Retreive answer
    # answer = response["answer"]
    # source = response["source_documents"]
    # st.write(answer)
    # st.write(source)
