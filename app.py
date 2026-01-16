import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="나만의 제미나이", page_icon="🤖")
st.title("🤖 나만의 제미나이 챗봇")

# 사이드바에 API 키 입력창 만들기 (보안을 위해)
with st.sidebar:
    user_api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    "[API 키 발급받기](https://aistudio.google.com/)"

if user_api_key:
    genai.configure(api_key=user_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("메시지를 입력하세요"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.info("왼쪽 사이드바에 API 키를 입력하면 대화를 시작할 수 있습니다.", icon="🔑")
