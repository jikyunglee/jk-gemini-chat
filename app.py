import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Jinkyung's Gemini Chat", page_icon="🤖")
st.title("🤖 Jinkyung's Gemini Chat")

with st.sidebar:
    user_api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    st.info("API 키를 입력하고 엔터를 눌러주세요.")

if user_api_key:
    try:
        genai.configure(api_key=user_api_key)
        
        # 가장 호환성이 높은 모델 이름을 직접 지정합니다.
        # 만약 flash가 안되면 pro로 자동 전환 시도하는 로직입니다.
        model_name = 'gemini-1.5-flash'
        model = genai.GenerativeModel(model_name)

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
                try:
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    # 에러가 나면 다른 모델(pro)로 한 번 더 시도합니다.
                    st.warning("Flash 모델 연결 실패. Pro 모델로 재시도합니다...")
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    
    except Exception as e:
        st.error(f"최종 에러 발생: {e}")
else:
    st.info("사이드바에 API 키를 넣어주세요.")
