import os
from dotenv import load_dotenv
from openai import OpenAI
import time
import streamlit as st

load_dotenv()
API_KEY = os.environ.get("API_KEY")

client = OpenAI(api_key=API_KEY)

thread_id = "thread_90GiVViN9D1lpBBwmRCS2mM6"
assistant_id = "asst_tfVGLRTf2pguUXgLd12yEC4d"

thread_messages = client.beta.threads.messages.list(thread_id)

st.header("chat")
# 기존 대화이력 로드
# for msg in reversed(thread_messages.data):
#     with st.chat_message(msg.role):
#         st.write(msg.content[0].text.value)

prompt = st.chat_input("questions?")
if prompt:
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )
    with st.chat_message(message.role):
        st.write(message.content[0].text.value)
    
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    while run.status != "completed":
        print("status 확인중", run.status)
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
    
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )

    with st.chat_message(messages.data[0].role):
        st.write(messages.data[0].content[0].text.value)
