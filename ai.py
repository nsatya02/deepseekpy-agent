# from autogen import UserProxyAgent, AssistantAgent
# from groq import Groq

# config_list =[{
#     "model":"deepseek-r1-distill-llama-70b",
#     "api_key":"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",
#     "api_type":"groq"
# }]

# assistant = AssistantAgent(
#     name="AI",
#     system_message="You are an helpful AI assistant",
#     llm_config={"config_list":config_list}
# )

# userproxy= UserProxyAgent(
#     name="user",
#     code_execution_config=False
# )

# def chat_assistant():
#     while True:
#         user_input=input("you:")
#         if user_input.lower() in ["exit","quit"]:
#             print("Ending chat")
#             break
#         response=userproxy.initiate_chat(assistant,message=user_input)
#         print("Assistant :",response)

# chat_assistant()

import streamlit as st
from autogen import UserProxyAgent, AssistantAgent
from groq import Groq

# LLM configuration
config_list = [{
    "model": "mixtral-8x7b-32768",
    "api_key": "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",
    "api_type": "groq"
}]

assistant = AssistantAgent(
    name="AI",
    system_message="You are a helpful AI assistant",
    llm_config={"config_list": config_list}
)

userproxy = UserProxyAgent(
    name="user",
    code_execution_config=False
)

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Custom CSS for a conversational UI
st.markdown(
    """
    <style>
    .chat-container {
        max-width: 800px;
        margin: 20px auto;
        padding: 20px;
        background: #ffffff;
        border-radius: 10px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
        overflow-y: auto;
        height: 500px;
    }
    .message {
        margin: 10px 0;
        padding: 10px 15px;
        border-radius: 15px;
        max-width: 70%;
        word-wrap: break-word;
    }
    .user {
        background-color: #DCF8C6;
        margin-left: auto;
        text-align: right;
    }
    .assistant {
        background-color: #ECECEC;
        margin-right: auto;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Chat with AI Assistant")
st.write("Enjoy a conversation-style chat experience below.")

# Chat display container
with st.container():
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"<div class='message user'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='message assistant'>{msg['content']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Input form for the conversation
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message:", key="user_input")
    submit_button = st.form_submit_button(label="Send")

if submit_button and user_input:
    # Append user message to the conversation
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Get assistant response and append it to the conversation
    with st.spinner("Assistant is thinking..."):
        # Initiate chat with AutoGen
        chat_response = userproxy.initiate_chat(
            assistant,
            message=user_input,
            clear_history=True  # Clear history for each new message
        )
        
        # Get the last message from the chat response
        if isinstance(chat_response, list) and len(chat_response) > 0:
            assistant_response = chat_response[-1].get('content', '')
        else:
            assistant_response = chat_response.messages[-1].get('content', '')
        
        # Append to chat history
        st.session_state.chat_history.append({
            "role": "assistant", 
            "content": assistant_response
        })
    
    # Force a rerun to update the UI
    st.rerun()
