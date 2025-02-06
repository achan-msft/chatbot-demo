import streamlit as st 
from app.converse import Converse


st.title("Welcome to the chatroom")

converse = Converse()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state['show_uploader'] = False
    system_message = converse.get_init_system_message()
    st.session_state.messages = system_message

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if "role" in message and message['role'] in ('assistant', 'user'):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

#----------------------------------------------------------------------------------------------------------------------------------
#   User input
#----------------------------------------------------------------------------------------------------------------------------------
if prompt := st.chat_input():    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):        
        message = converse.start(message_list=st.session_state.messages, is_stream=False)
        st.markdown(message)

    st.session_state.messages.append({"role": "assistant", "content": message})
