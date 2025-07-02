from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain.llms import OpenAI
from langchain.schema import HumanMessage

# LLMからの回答を取得する関数
def get_llm_response(input_text, language_choice):
    # OpenAI LLMの初期化（API キーは環境変数から取得）
    llm = OpenAI(temperature=0.7)
    
    # プロンプトの設定
    if language_choice == "A":
        prompt = f"関西弁で答えてください。質問: {input_text}"
    else:  # B
        prompt = f"標準語で丁寧に答えてください。質問: {input_text}"
    
    # LLMに問い合わせ
    response = llm(prompt)
    return response

# Streamlitアプリのメイン部分
def main():
    st.title("LLMチャットアプリ")
    st.write("これは試作です、AかBのラジオボタンを選び、質問してください")
    
    # ラジオボタンの設定
    language_option = st.radio(
        "回答スタイルを選択してください：",
        ("A", "B"),
        help="A: 関西弁、B: 標準語"
    )
    
    # 入力フォーム
    user_input = st.text_input("質問を入力してください：")
    
    # 送信ボタン
    if st.button("送信"):
        if user_input:
            try:
                # LLMからの回答を取得
                with st.spinner("回答を生成中..."):
                    response = get_llm_response(user_input, language_option)
                
                # 回答を表示
                st.subheader("回答：")
                st.write(response)
                
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")
        else:
            st.warning("質問を入力してください")

if __name__ == "__main__":
    main()