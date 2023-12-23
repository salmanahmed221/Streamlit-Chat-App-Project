import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


if "messages" not in st.session_state:
    st.session_state.messages = []

st.write(st.session_state.messages)
for my_message in st.session_state.messages:
    with st.chat_message(my_message["role"]):
        st.write(my_message["content"])

prompt = st.chat_input("Ask me anything")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream = True    
        )
        for i in response:
            print(i.choices[0].delta.content or "")
            full_response += (i.choices[0].delta.content or "")
            message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})