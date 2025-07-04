import streamlit as st
import pandas as pd
from datetime import date, datetime

# CSVまたはExcelファイルの読み込み（年月日分割対応）
@st.cache_data
def load_data():
    return pd.read_excel("子育て支援制度テンプレート_年月日分割版.xlsx")

df = load_data()

# タイトル＆説明
st.title("あなたが受け取れる子育て支援制度を今すぐチェック")
st.write("数問に答えるだけで、あなたに合った制度がわかります")

# ユーザー入力フォーム
with st.form("user_input_form"):
    st.subheader("かんたんステップ")

    # Step 1: 居住地（都道府県）
    prefecture = st.selectbox("都道府県を選んでください", df["都道府県"].unique())

    # Step 2: 市区町村
    municipalities = df[df["都道府県"] == prefecture]["市区町村"].unique()
    city = st.selectbox("市区町村を選んでください", municipalities)

    # Step 3: 子どもの年齢（任意）
    child_age = st.slider("お子さまの年齢（任意）", 0, 18, 3)

    # Step 4: 勤務状況（任意）
    work_status = st.selectbox("現在の勤務状況", ["共働き", "片働き", "専業主婦(夫)", "育休中", "その他"])

    # Step 5: 生年月日（新機能）
    dob = st.date_input("お子さまの生年月日を入力してください", min_value=date(2000, 1, 1), max_value=date.today())

    submitted = st.form_submit_button("制度を見つける")

if submitted:
    st.subheader("あなたに合いそうな制度はこちら")

    # 生年月日による対象判定
    def is_dob_within_range(row, dob):
        try:
            from_date = datetime(int(row["生年_from"]), int(row["月_from"]), int(row["日_from"]))
            to_date = datetime(int(row["生年_to"]), int(row["月_to"]), int(row["日_to"]))
            return from_date <= dob <= to_date
        except:
            return False

    # 条件にマッチする制度を抽出
    filtered = df[
        (df["市区町村"] == city) &
        df.apply(lambda row: is_dob_within_range(row, dob), axis=1)
    ]

    if filtered.empty:
        st.warning("該当する制度が見つかりませんでした。条件を変更してお試しください。")
    else:
        for _, row in filtered.iterrows():
            with st.expander(row["制度名"]):
                st.markdown(f"**対象区分:** {row['対象区分']}")
                st.markdown(f"**条件補足:** {row['条件補足']}")
                st.markdown(f"**申請期限:** {row['申請期限']}")
                st.markdown(f"[申請ページに進む]({row['制度リンク']})")

