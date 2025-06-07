import streamlit as st
import pandas as pd
import numpy as np
from persiantools.jdatetime import JalaliDate
import base64

st.set_page_config(page_title="تحلیل عملکرد واحدهای سازمانی", layout="centered")

# استایل
st.markdown("""
<style>
* {
    font-family: Tahoma, sans-serif !important;
}
html, body, [class*='css'] {
    background-color: #3a3a3a;
    color: #ffffff;
}
.stButton > button {
    color: white !important;
    background-color: #2563eb !important;
}
</style>
""", unsafe_allow_html=True)

st.image("logo.png", width=100)
st.markdown(f"تاریخ امروز: {JalaliDate.today().strftime('%Y/%m/%d')}")

# خوش‌آمد
if "شروع" not in st.session_state:
    st.session_state["شروع"] = False

if not st.session_state["شروع"]:
    st.markdown("""
    ## تحلیل عملکرد واحدهای سازمانی

    این نرم‌افزار به شما امکان می‌دهد تا عملکرد واحدهای مختلف سازمان را با استفاده از شاخص‌های کلیدی عمومی و اختصاصی، به صورت کمی تحلیل کرده و نتایج را رتبه‌بندی کنید.

    ### ساختار تحلیل:
    - شاخص‌های عمومی: اهداف، بهره‌وری، هزینه، رضایت، تعامل و خطا
    - شاخص‌های تخصصی: متناسب با نوع فعالیت هر واحد قابل تعریف است (تا سه شاخص)
    - امتیاز کل و امتیاز سرانه‌ای (براساس تعداد نیرو)

    تحلیل بر مبنای مدل وزنی AHP انجام شده و خروجی شامل رتبه‌بندی و تحلیل نقاط قوت است.
    """)

    st.markdown("توسعه‌یافته توسط <a href='https://inohub.ir' target='_blank'>اینوهاب</a>", unsafe_allow_html=True)
    if st.button("شروع"):
        st.session_state["شروع"] = True
    st.stop()

# حالت انتخاب ورود داده‌ها
mode = st.radio("چگونه می‌خواهید داده‌ها را وارد کنید؟", ["بارگذاری فایل اکسل", "ورود آنلاین اطلاعات"])

if mode == "بارگذاری فایل اکسل":
    with open("نمونه_تحلیل_واحدهای_سازمانی.xlsx", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="نمونه_تحلیل_واحدهای_سازمانی.xlsx" style="color:#93c5fd;">دانلود فایل نمونه اکسل</a>'
        st.markdown(href, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("فایل اکسل را بارگذاری کنید", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.success("فایل با موفقیت بارگذاری شد.")
        with open("نمونه_تحلیل_واحدهای_سازمانی.xlsx", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="نمونه_تحلیل_واحدهای_سازمانی.xlsx" style="color:#93c5fd;">دانلود فایل نمونه اکسل</a>'
            st.markdown(href, unsafe_allow_html=True)

elif mode == "ورود آنلاین اطلاعات":
    st.info("تعداد واحدهایی که می‌خواهید وارد کنید را مشخص نمایید")
    count = st.number_input("تعداد واحدها", min_value=1, max_value=20, value=4)
    inputs = []
    for i in range(count):
        with st.expander(f"واحد {i+1}"):
            name = st.text_input(f"نام واحد {i+1}", key=f"n_{i}")
            people = st.number_input("تعداد نیرو", min_value=1, value=5, key=f"p_{i}")
            g1 = st.slider("دستیابی به اهداف", 0, 10, 5, key=f"g1_{i}")
            g2 = st.slider("بهره‌وری منابع", 0, 10, 5, key=f"g2_{i}")
            g3 = st.slider("هزینه / سودآوری", 0, 10, 5, key=f"g3_{i}")
            g4 = st.slider("رضایت مشتریان داخلی", 0, 10, 5, key=f"g4_{i}")
            g5 = st.slider("سرعت پاسخ‌گویی", 0, 10, 5, key=f"g5_{i}")
            g6 = st.slider("نوآوری / بهبود فرآیند", 0, 10, 5, key=f"g6_{i}")
            g7 = st.slider("تعامل بین‌واحدی", 0, 10, 5, key=f"g7_{i}")
            g8 = st.slider("میزان خطا", 0, 10, 5, key=f"g8_{i}")
            s1 = st.slider("شاخص تخصصی ۱", 0, 10, 5, key=f"s1_{i}")
            s2 = st.slider("شاخص تخصصی ۲", 0, 10, 5, key=f"s2_{i}")
            s3 = st.slider("شاخص تخصصی ۳", 0, 10, 5, key=f"s3_{i}")
            inputs.append({
                "نام واحد": name,
                "تعداد نیرو": people,
                "دستیابی به اهداف": g1,
                "بهره‌وری منابع": g2,
                "هزینه / سودآوری": g3,
                "رضایت مشتریان داخلی": g4,
                "سرعت پاسخ‌گویی": g5,
                "نوآوری / بهبود فرآیند": g6,
                "تعامل بین‌واحدی": g7,
                "میزان خطا": g8,
                "شاخص تخصصی ۱": s1,
                "شاخص تخصصی ۲": s2,
                "شاخص تخصصی ۳": s3
            })
    if st.button("تحلیل اطلاعات"):
        df = pd.DataFrame(inputs)
        st.success("اطلاعات ثبت شد.")

        st.subheader("وزن‌دهی به شاخص‌ها")
        weights = {}
        columns = df.columns[2:]
        for col in columns:
            weights[col] = st.slider(f"اهمیت {col}", 1, 10, 5)

        weight_array = np.array([weights[c] for c in columns])
        weight_array = weight_array / weight_array.sum()
        score_matrix = df[columns].values
        weighted_scores = np.dot(score_matrix, weight_array)

        df["امتیاز کل"] = weighted_scores.round(2)
        df["امتیاز سرانه"] = (df["امتیاز کل"] / df["تعداد نیرو"]).round(2)

        st.subheader("نتیجه رتبه‌بندی واحدها")
        sorted_df = df.sort_values(by="امتیاز سرانه", ascending=False).reset_index(drop=True)
        sorted_df.index += 1
        st.dataframe(sorted_df)

        st.subheader("تحلیل هوشمند واحد برتر")
        top_unit = sorted_df.iloc[0]
        top_name = top_unit["نام واحد"]
        st.markdown(f"🔍 واحد **{top_name}** بالاترین امتیاز سرانه را کسب کرده است.")
        for col in columns:
            val = top_unit[col]
            if val >= 8:
                st.markdown(f"- شاخص **{col}** با امتیاز {val} نشان‌دهنده عملکرد بسیار قوی است.")
            elif val <= 4:
                st.markdown(f"- شاخص **{col}** با امتیاز {val} نیازمند بررسی و بهبود است.")
