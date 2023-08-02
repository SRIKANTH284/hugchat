import streamlit as st
import requests
from hugchat import hugchat
from hugchat.login import Login

# App title
st.set_page_config(page_title="🤗💬 HugChat")

# Hugging Face Credentials
with st.sidebar:
    st.title('🤗💬 HugChat')
    if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
        st.success('HuggingFace Login credentials already provided!', icon='✅')
        hf_email = st.secrets['EMAIL']
        hf_pass = st.secrets['PASS']
    else:
        hf_email = st.text_input('Enter E-mail:', type='password')
        hf_pass = st.text_input('Enter password:', type='password')
        if not (hf_email and hf_pass):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    
    
# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating LLM response
def generate_response(prompt_input, email, passwd):
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    # Create ChatBot                        
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt_input)

# Function to perform a web search
def perform_web_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    response = requests.get(search_url)
    return response.text

# User-provided prompt
if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Check if user's message is a search request
    if prompt.lower().startswith("search:"):
        search_query = prompt[len("search:"):].strip()
        with st.chat_message("assistant"):
            with st.spinner("Searching..."):
                search_result = perform_web_search(search_query)
                st.write(search_result)
    else:
        # Generate a new response if the last message is not from the assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_response(prompt, hf_email, hf_pass) 
                    st.write(response)
                    message = {"role": "assistant", "content": response}
                    st.session_state.messages.append(message)
                    
                    # Display balloons when assistant sends a response
                    st.balloons()