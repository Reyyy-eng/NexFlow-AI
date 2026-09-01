import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(
    page_title="NexFlow AI",
    page_icon="🚦",
    layout="centered"
)

# بيانات التدريب
data = {
    "cars": [
        10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
        15, 25, 35, 45, 55, 65, 75, 85, 95
    ],

    "speed": [
        100, 90, 80, 70, 60, 50, 40, 30, 20, 10,
        95, 85, 75, 65, 55, 45, 35, 25, 15
    ],

    "traffic": [
        "منخفض", "منخفض", "منخفض", "متوسط", "متوسط",
        "مرتفع", "مرتفع", "مرتفع", "مرتفع", "مرتفع",
        "منخفض", "متوسط", "متوسط", "متوسط", "مرتفع",
        "مرتفع", "مرتفع", "مرتفع", "مرتفع"
    ]
}

df = pd.DataFrame(data)

X = df[["cars", "speed"]]
y = df["traffic"]

# إنشاء نموذج الذكاء الاصطناعي
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# عنوان التطبيق
st.title("🚦 NexFlow AI")
st.header("نظام ذكي للتنبؤ بحالة حركة المرور 🚗")
st.write("أدخل عدد السيارات ومتوسط السرعة لتحليل حالة الطريق والتنبؤ بمستوى الازدحام.")

st.divider()

# إدخال البيانات
cars = st.number_input(
    "🚗 عدد السيارات",
    min_value=0,
    max_value=500,
    value=200,
    step=1
)

speed = st.number_input(
    "⚡ متوسط السرعة (كم/س)",
    min_value=0.0,
    max_value=150.0,
    value=45.0,
    step=1.0
)

# زر التحليل
if st.button("🔍 تحليل حركة المرور", use_container_width=True):

    prediction = model.predict([[cars, speed]])[0]

    probability = (
        model.predict_proba([[cars, speed]])[0].max() * 100
    )
    st.info("🤖 تم تحليل بيانات الطريق باستخدام الذكاء الاصطناعي")
    st.divider()

    # عرض حالة المرور
    if prediction == "مرتفع":
        st.error("🔴 حالة المرور: مزدحمة")

    elif prediction == "متوسط":
        st.warning("🟠 حالة المرور: متوسطة")

    else:
        st.success("🟢 حالة المرور: منخفضة")

    # عرض البيانات
    col1, col2 = st.columns(2)

    with col1:
        st.metric("🚗 السيارات", cars)

    with col2:
        st.metric("⚡ السرعة", f"{speed:.1f} كم/س")

    st.metric(
        "🎯 نسبة الثقة",
        f"{probability:.1f}%"
    )

    st.divider()

    # جدول النتائج
    result = pd.DataFrame({
        "البيان": [
            "عدد السيارات",
            "متوسط السرعة",
            "حالة المرور"
        ],

        "القيمة": [
    str(cars),
    str(float(speed)),
    str(prediction)
]
    })

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True
    )

st.divider()

st.caption("NexFlow AI • Smart Traffic Prediction")
st.subheader("📊 تحليل بيانات المرور")



chart_data = pd.DataFrame({
    "القيمة": [float(cars), float(speed)]
}, index=["عدد السيارات", "السرعة"])

st.bar_chart(chart_data)