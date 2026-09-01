import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# بيانات حركة المرور
data = {
    "cars": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
             15, 25, 35, 45, 55, 65, 75, 85, 95],
    "speed": [100, 90, 80, 70, 60, 50, 40, 30, 20, 10,
              95, 85, 75, 65, 55, 45, 35, 25, 15],
    "traffic": [
        "منخفض", "منخفض", "منخفض", "متوسط", "متوسط",
        "متوسط", "مرتفع", "مرتفع", "مرتفع", "مرتفع",
        "منخفض", "منخفض", "متوسط", "متوسط", "متوسط",
        "مرتفع", "مرتفع", "مرتفع", "مرتفع"
    ]
}

df = pd.DataFrame(data)

# خصائص التدريب
X = df[["cars", "speed"]]
y = df["traffic"]

# تدريب نموذج AI
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X, y)

# حالة الطريق الحالية
cars = int(input("🚗 أدخل عدد السيارات: "))
speed = float(input("⚡ أدخل متوسط السرعة كم/س: "))

# التوقع
prediction = model.predict([[cars, speed]])[0]
probability = model.predict_proba([[cars, speed]])[0].max() * 100

print("🚦 NexFlow AI")
print("====================")
print(f"🚗 عدد السيارات: {cars}")
print(f"⚡ السرعة: {speed} كم/س")
print(f"📊 التوقع: {prediction}")
print(f"🎯 الثقة: {probability:.1f}%")