import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="Jinkyung's Gemini Chat", page_icon="🤖")
st.title("🤖 Jinkyung's Gemini Chat")

# 사이드바 설정
with st.sidebar:
    # 1. API 키 입력 (직접 입력 혹은 Streamlit Secrets 사용)
    user_api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    st.markdown("[API 키 발급받기](https://aistudio.google.com/)")
    
    # 2. 모델 선택 (에러 방지를 위해 선택권 부여)
    model_option = st.selectbox("모델을 선택하세요", ["gemini-1.5-flash", "gemini-pro"])

if user_api_key:
    try:
        genai.configure(api_key=user_api_key)
        
        # 선택한 모델로 초기화
        model = genai.GenerativeModel(model_option)

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
                try:
                    # 답변 생성
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"대화 중 에러 발생: {e}")
                    st.info("왼쪽 메뉴에서 'gemini-pro'로 모델을 바꿔서 다시 시도해보세요.")
                    
    except Exception as e:
        st.error(f"연결 에러: {e}")
else:
    st.info("왼쪽 사이드바에 API 키를 입력해주세요.")
