import streamlit as st
from streamlit_chat import message
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from conf.questions import sample_q
from utils import make_chain, DB_DIR
from ui import header_ui

# set page config

st.set_page_config(page_title="Mapletree GPT", page_icon=":robot_face:")
# Hide footer made with Streamlit
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
header_ui()
st.write("##")
# Initialise session state variables
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        SystemMessage(content="You are a helpful assistant.")
    ]

# Sidebar - let user choose model, show total cost of current conversation, and let user clear the current conversation
model = "gpt-4"
with st.sidebar:
    api_key = st.text_input(label="Enter Open AI API Key")


# generate a response
def generate_response(prompt, api_key, DB_DIR=DB_DIR):
    # st.session_state["messages"].append({"role": "user", "content": prompt})
    chat_chain = make_chain(api_key=api_key, db_dir=DB_DIR)
    response = chat_chain({"question": prompt, "chat_history": []})
    return response


# # container for chat history
response_container = st.container()
# container for text box
container = st.container()
with container:
    samp_select = st.selectbox(label="Select sample questions", options=sample_q)
    with st.form(key="my_form", clear_on_submit=True):
        if samp_select:
            user_input = st.text_area(
                "query:", value=samp_select, key="input", height=100
            )
        else:
            user_input = st.text_area("query:", key="input", height=100)
        submit_button = st.form_submit_button(label="Send")

    if submit_button and user_input and api_key:
        st.session_state.messages.append(HumanMessage(content=user_input))
        response = generate_response(user_input, api_key=api_key, DB_DIR=DB_DIR)
        # st.write(response)
        st.session_state.messages.append(AIMessage(content=response["answer"]))

    with response_container:
        messages = st.session_state.get("messages", [])
        for i, msg in enumerate(messages[1:]):
            if i % 2 == 0:
                # st.write(msg)
                message(msg.content, is_user=True, key=str(i) + "_user")
            else:
                # st.write(dir(msg))
                message(msg.content, is_user=False, key=str(i) + "_ai")
