#=====================
#Chainlit Version
#=====================
# import chainlit as cl
# import ollama

# @cl.on_chat_start
# async def start_chat():
#     cl.user_session.set(
#         "interaction",
#         [
#             {
#                 "role": "system",
#                 "content": "You are a helpful assistant.",
#             }
#         ],
#     )

#     await cl.Message(content="Hello, I'm your local AI assistant. How can I help you today?").send()

# @cl.on_message 
# async def main(message: cl.Message):
#     # Get current chat history
#     interaction = cl.user_session.get("interaction")
    
#     # Add user message to interaction
#     interaction.append({
#         "role": "user",
#         "content": message.content
#     })

#     try:
#         # Create message placeholder
#         msg = cl.Message(content="")
#         await msg.send()

#         # Get response from Ollama
#         response = ollama.chat(
#             model="deepseek-r1:14b",
#             messages=interaction,
#             stream=True  # Enable streaming
#         )
        
#         # Stream the response
#         for chunk in response:
#             content = chunk['message']['content']
#             await msg.stream_token(content)
        
#         # Store assistant's response
#         interaction.append({
#             "role": "assistant",
#             "content": msg.content
#         })
        
#         await msg.update()
        
#     except Exception as e:
#         print(f"Error: {str(e)}")  # Print error to console
#         await cl.Message(content=f"Error: {str(e)}").send()

#=====================
# Streamlit Version
#=====================

# import streamlit as st
# import ollama

# # Initialize session state for chat history
# if "interaction" not in st.session_state:
#     st.session_state.interaction = [
#         {
#             "role": "system",
#             "content": "You are a helpful assistant.",
#         }
#     ]

# # Function to display chat messages
# def display_chat():
#     for message in st.session_state.interaction:
#         if message["role"] == "user":
#             st.markdown(f"<div style='text-align: right; color: blue;'>{message['content']}</div>", unsafe_allow_html=True)
#         else:
#             st.markdown(f"<div style='text-align: left; color: green;'>{message['content']}</div>", unsafe_allow_html=True)

# # Streamlit app layout
# st.title("Chat with AI Assistant")
# st.write("Enjoy a conversation-style chat experience below.")

# # Display chat history
# display_chat()

# # User input form
# user_input = st.text_input("Your message:", key="user_input", value="")

# if st.button("Send"):
#     # Append user message to interaction
#     st.session_state.interaction.append({
#         "role": "user",
#         "content": user_input
#     })

#     # Get response from Ollama
#     try:
#         response = ollama.chat(
#             model="deepseek-r1:14b",
#             messages=st.session_state.interaction
#         )
        
#         # Store assistant's response
#         assistant_response = response['message']['content']
#         st.session_state.interaction.append({
#             "role": "assistant",
#             "content": assistant_response
#         })
        
#     except Exception as e:
#         st.session_state.interaction.append({
#             "role": "assistant",
#             "content": f"Error: {str(e)}"
#         })

#     # Clear the input box by setting the value to an empty string
#     st.rerun()  # Refresh the app to update the UI