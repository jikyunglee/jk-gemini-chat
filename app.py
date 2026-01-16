import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Jinkyung's Gemini Chat", page_icon="🤖")
st.title("🤖 Jinkyung's Gemini Chat")

# 사이드바 설정
with st.sidebar:
    user_api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    st.info("새로 발급받은 키를 입력해주세요.")

if user_api_key:
    try:
        # API 설정 (가장 표준적인 방식)
        genai.configure(api_key=user_api_key)
        
        # 모델 설정 (가장 기본 이름만 사용)
        model = genai.GenerativeModel('gemini-1.5-flash')

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("질문을 입력하세요"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # 실제 답변 생성 구간
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                    
    except Exception as e:
        # 에러 발생 시 메시지 출력
        st.error(f"에러가 발생했습니다: {e}")
else:
    st.info("사이드바에 API 키를 넣어주세요.")
        st.error(f"최종 에러 발생: {e}")
else:
    st.info("사이드바에 API 키를 넣어주세요.")
