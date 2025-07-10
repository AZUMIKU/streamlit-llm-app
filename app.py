import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from openai import OpenAI
import os

from dotenv import load_dotenv
load_dotenv()

# OpenAI APIキーの確認
if not os.getenv("OPENAI_API_KEY"):
    st.error("OpenAI API キーが設定されていません。.envファイルを確認してください。")
    st.stop()


def get_expert_response(user_input, expert_type):
    """LLMからの回答を返す関数"""
    
    # 専門家タイプに応じてシステムメッセージを設定
    if expert_type == 'プログラミング専門家':
        system_message = "あなたはプログラミングの専門家です。技術的な質問に詳しく答えてください。"
    else:  # 料理専門家
        system_message = "あなたは料理の専門家です。料理に関する質問に詳しく答えてください。"
    
    try:
        # 直接OpenAIクライアントを使用
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# Streamlitアプリ
st.title("専門家チャットアプリ")

st.markdown("""
## 使い方
1. 専門家を選択
2. 質問を入力
3. 「回答を取得」ボタンをクリック
""")

# 専門家選択
expert_type = st.radio(
    "専門家を選択してください:",
    ["プログラミング専門家", "料理専門家"]
)

# 質問入力
user_input = st.text_area(
    "質問を入力してください:",
    height=100,
    placeholder="例: Pythonのリスト操作について教えて"
)

# 回答取得ボタン
if st.button("回答を取得"):
    if user_input.strip():
        with st.spinner("回答を生成中..."):
            response = get_expert_response(user_input, expert_type)
            st.subheader(f"{expert_type}の回答:")
            st.write(response)
    else:
        st.warning("質問を入力してください。")