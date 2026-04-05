import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="AI Finance Analyzer", layout="wide")

st.title("💰 AI Behavioral Finance Analyzer")
st.markdown("### Understand your *spending behavior* & hidden financial patterns")

# ---------------------------
# LOAD DATA
# ---------------------------
df = pd.read_csv("data.csv")
df["Date"] = pd.to_datetime(df["Date"])

# ---------------------------
# BASIC METRICS
# ---------------------------
total_spending = df["Amount"].sum()
avg = df["Amount"].mean()

col1, col2 = st.columns(2)

with col1:
    st.metric("💸 Total Spending", f"₹{total_spending}")

with col2:
    st.metric("📊 Average Spending", f"₹{round(avg,2)}")

# ---------------------------
# CATEGORY ANALYSIS
# ---------------------------
st.subheader("📊 Spending by Category")

category_sum = df.groupby("Category")["Amount"].sum()

fig, ax = plt.subplots()
category_sum.plot(kind='bar', color='skyblue', ax=ax)
plt.title("Category-wise Spending")
st.pyplot(fig)

# ---------------------------
# TREND ANALYSIS
# ---------------------------
st.subheader("📈 Spending Trend")

df["Day"] = range(1, len(df)+1)

fig2, ax2 = plt.subplots()
ax2.plot(df["Day"], df["Amount"], marker='o')
ax2.set_title("Spending Trend Over Time")
st.pyplot(fig2)

# ---------------------------
# ANOMALY DETECTION
# ---------------------------
st.subheader("🚨 Unusual Spending Detection")

threshold = avg * 1.5
anomalies = df[df["Amount"] > threshold]

if not anomalies.empty:
    st.error("Unusual high spending detected!")
    st.write(anomalies)
else:
    st.success("No unusual spending")

# ---------------------------
# USER PERCEPTION INPUT
# ---------------------------
st.subheader("🧠 Your Perception")

avg_perception = st.slider("How do you feel about your spending? (1 = low, 10 = high)", 1, 10, 5)

# ---------------------------
# PERCEPTION vs REALITY
# ---------------------------
st.subheader("⚖️ Perception vs Reality")

if avg_perception > 7 and avg > 500:
    st.warning("⚠️ You are underestimating your spending!")
elif avg_perception < 5 and avg < 500:
    st.info("You may be overestimating your spending")
else:
    st.success("Your perception matches your actual spending")

# ---------------------------
# SMART INSIGHTS
# ---------------------------
st.subheader("🧠 Smart Insights")

shopping = df[df["Category"] == "Shopping"]["Amount"].sum()
food = df[df["Category"] == "Food"]["Amount"].sum()

if shopping > food:
    st.write("🛍️ You spend more on Shopping than Food")

if df["Amount"].iloc[-1] > df["Amount"].iloc[0]:
    st.write("📈 Your spending is increasing over time")

# ---------------------------
# PREDICTION (Simple AI)
# ---------------------------
st.subheader("🔮 Future Spending Prediction")

predicted = avg * 1.1
st.write(f"Estimated next period spending: ₹{int(predicted)}")

# ---------------------------
# RISK SCORE
# ---------------------------
st.subheader("⚠️ Financial Risk Score")

risk = 0

if total_spending > avg:
    risk += 40

if len(anomalies) > 1:
    risk += 30

if avg_perception > 7:
    risk += 30

st.metric("Risk Score", f"{risk}/100")

if risk > 70:
    st.error("💥 High Financial Risk")
elif risk > 40:
    st.warning("⚠️ Moderate Risk")
else:
    st.success("✅ Low Risk")

# ---------------------------
# FINANCIAL PERSONALITY
# ---------------------------
st.subheader("🧬 Your Financial Personality")

if risk > 70:
    st.write("💥 High Risk Spender")
elif risk > 40:
    st.write("⚠️ Moderate Spender")
else:
    st.write("✅ Controlled Spender")

# ---------------------------
# EXTRA ALERT
# ---------------------------
if avg > 700:
    st.write("⚠️ High spending detected overall")