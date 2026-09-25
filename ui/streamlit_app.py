import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000').rstrip('/')

st.set_page_config(
    page_title='Agentic Chatbot',
    page_icon='🤖',
    layout='centered',
)

st.title('🤖 Agentic Chatbot')
st.caption('Streamlit UI -> FastAPI -> LangGraph Agent -> Tools -> Response')

with st.sidebar:
    st.subheader('Backend')
    st.code(BACKEND_URL)
    st.write('Tools: calculator, current time, weather')
    if st.button('Clear chat'):
        st.session_state.messages = []
        st.rerun()

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

prompt = st.chat_input('Ask something...')

if prompt:
    with st.chat_message('user'):
        st.markdown(prompt)

    history = st.session_state.messages.copy()
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    with st.chat_message('assistant'):
        with st.spinner('Agent is working...'):
            try:
                response = requests.post(
                    f'{BACKEND_URL}/chat',
                    json={'message': prompt, 'history': history},
                    timeout=120,
                )
                response.raise_for_status()
                data = response.json()
                answer = data['answer']
                tool_calls = data.get('tool_calls', [])

                st.markdown(answer)
                if tool_calls:
                    st.caption('Tools used: ' + ', '.join(tool_calls))

                st.session_state.messages.append(
                    {'role': 'assistant', 'content': answer}
                )
            except requests.RequestException as exc:
                st.error(f'Backend connection failed: {exc}')
            except Exception as exc:
                st.error(f'Unexpected error: {exc}')