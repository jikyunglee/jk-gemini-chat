import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="Jinkyung's Gemini Chat", page_icon="🤖")
st.title("🤖 Jinkyung's Gemini Chat")

# 2. 사이드바 설정
with st.sidebar:
    user_api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    st.markdown("[API 키 발급받기](https://aistudio.google.com/)")

if user_api_key:
    try:
        # API 설정
        genai.configure(api_key=user_api_key)
        
        # 모델 설정 (이름 앞에 models/를 붙여 더 정확하게 지정합니다)
        model = genai.GenerativeModel('models/gemini-1.5-flash')

        # 채팅 기록 초기화
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # 기존 대화 표시
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 사용자 입력
        if prompt := st.chat_input("메시지를 입력하세요"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # 답변 생성
            with st.chat_message("assistant"):
                try:
                    # 답변을 생성하는 핵심 구간
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    # 에러가 나면 화면에 빨간 박스로 표시해줍니다.
                    st.error(f"대화 중 에러가 발생했습니다: {e}")
                    st.info("API 키가 최신 모델(1.5 Flash)을 지원하는지 확인해주세요.")
                    
    except Exception as e:
        st.error(f"설정 중 에러가 발생했습니다: {e}")
else:
    st.info("왼쪽 사이드바에 API 키를 입력하면 대화를 시작할 수 있습니다.", icon="🔑")
