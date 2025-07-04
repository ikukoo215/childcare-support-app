import streamlit as st
import pandas as pd
from datetime import date

# CSVファイルの読み込み（例：制度データ）
@st.cache_data
def load_data():
    return pd.read_csv("support_programs.csv")

df = load_data()

# タイトル＆説明
st.title("あなたが受け取れる子育て支援制度を今すぐチェック")
st.write("数問に答えるだけで、あなたに合った制度がわかります")

# ユーザー入力フォーム
with st.form("user_input_form"):
    st.subheader("かんたん3ステップ")

    # Step 1: 居住地
    prefecture = st.selectbox("都道府県を選んでください", df["都道府県"].unique())

    # Step 2: 市区町村
    municipalities = df[df["都道府県"] == prefecture]["市区町村"].unique()
    city = st.selectbox("市区町村を選んでください", municipalities)

    # Step 3: 子どもの年齢
    child_age = st.slider("お子さまの年齢（半角数字で）", 0, 18, 3)

    # Step 4: 勤務状況（任意）
    work_status = st.selectbox("現在の勤務状況", ["共働き", "片働き", "専業主婦(夫)", "育休中", "その他"])

    submitted = st.form_submit_button("制度を見つける")

if submitted:
    st.subheader("あなたに合いそうな制度はこちら")

    # 条件でフィルタリング（例：市区町村と年齢）
    results = df[(df["市区町村"] == city) & (df["対象年齢"] >= child_age)]

    if results.empty:
        st.warning("該当する制度が見つかりませんでした。条件を変更してお試しください。")
    else:
        for _, row in results.iterrows():
            with st.expander(row["制度名"]):
                st.markdown(f"**概要:** {row['概要']}")
                st.markdown(f"**対象条件:** {row['対象条件']}")
                st.markdown(f"**申請期限:** {row['申請期限']}")
                st.markdown(f"[申請ページに進む]({row['申請リンク']})")
                if row['申請期限']:
                    st.button(f"📅 Googleカレンダーに登録（予定）", key=row['制度名'])
