import os, json
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai 

# SETUP
load_dotenv()
API = os.getenv("API")
genai.configure(api_key=API)

# LOAD CONFIG
with open("config.json", 'r', encoding="utf-8") as f:
    config = json.load(f)

    funcs = config.get("function", "giới thiệu nhà hàng")
    initial_message = config.get("initial_bot_message", "Tôi có thể giúp bạn điều gì?")

df = pd.read_csv("menu.csv")

# SETUP CONTEXT
model = genai.GenerativeModel("gemini-1.5-flash",
                            system_instruction=f"""Bạn tên là MenuBot, nhiệm vụ của bạn là đưa
                            ra menu dưới dạng bảng |Tên món ăn|Mô tả|Nguyên liệu|Ghi chú|,
                            giải đáp thắc mắc và hỗ trợ khách hàng theo yêu cầu của họ
                            Trong menu gồm {','.join(df["name"])}
                            Nếu không thể hỗ trợ, hãy kêu người dùng liên lạc đến 
                            số 666-666-6666
                            """)

# INTERFACE
def chatbot():
    st.title("Restaurant Bot")
    st.write("Hello, how can I help you?")

    # If history doesn't exist
    if 'history' not in st.session_state:
        st.session_state.history = [
            {"role" : "assistant", 
             "content" : initial_message}
        ]

    # else
    for message in st.session_state.history:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.write(message["content"])

    if prompt := st.chat_input("Your message"):
        with st.chat_message("user"):
            st.write(prompt)

        # add to history
        st.session_state.history.append({
            "role" : "user",
            "content" : prompt
        })

        # LLM creates response
        response = model.generate_content(prompt)
        bot_reply = response.text

        with st.chat_message("assistant"):
            st.write(bot_reply)

        #add to history
        st.session_state.history.append({
            "role": "assistant",
            "content": bot_reply
        })
    
if __name__ == "__main__":
    chatbot()

