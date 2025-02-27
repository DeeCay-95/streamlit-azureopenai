import streamlit as st
import requests
import json

subscription_key = "27f91eb6c5b042c293d81810c5e92ab4"

# Azure OpenAI API details
url = f"https://apim-azureopenai-i1.azure-api.net/azureopenaiapitest/openai/deployments/gpt-4o-mini-test/chat/completions?api-version=2024-02-15-preview&subscription-key={subscription_key}"
headers = {
    'Content-Type': 'application/json'
}

# Streamlit App Title
st.title("Lincon OpenAI Chatbot")

# User options for parameters
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.05)
top_p = st.sidebar.slider("Top P", 0.0, 1.0, 0.95, 0.05)
max_tokens = st.sidebar.number_input("Max Tokens", min_value=1, max_value=4096, value=800)

def llm_call(messages):
    payload = json.dumps({
    "messages": [
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": "You are an AI assistant that helps people find information."
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": f"{messages}"
            }
        ]
        }  ],
    "temperature": temperature,
    "top_p": top_p,
    "max_tokens": max_tokens
    })
    
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Error: Unable to get response from API."

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an AI assistant that helps people find information."}
    ]

# Display chat history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask me anything!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = llm_call(st.session_state.messages)
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
