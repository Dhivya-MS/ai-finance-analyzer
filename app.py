import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="AI Finance Pro", layout="wide")

# ---------------------------
# PREMIUM UI CSS
# ---------------------------
st.markdown("""
<style>
body {background-color: #0e1117;}
h1, h2, h3 {color: white;}
.stMetric {background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# LOGIN SYSTEM
# ---------------------------
import streamlit as st

# Session state create
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# LOGIN UI
if not st.session_state.logged_in:
    st.title("🔐 Login to AI Finance Analyzer")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login successful ✅")
        else:
            st.error("Invalid credentials ❌")

# AFTER LOGIN (MAIN APP)
else:
    st.title("💰 AI Behavioral Finance Analyzer")

    st.success("Welcome bro 😎🔥")

    st.write("Now your dashboard will come here...")

    # Example:
    st.write("👉 Total Spending: ₹6750")
    st.write("👉 Avg Spending: ₹675")

    if st.button("Logout"):
        st.session_state.logged_in = False

# ---------------------------
# TITLE
# ---------------------------
st.title("💰 AI-Based Financial Risk & Behavior Analyzer")
st.markdown("### 🔍 Smart AI insights into your spending")

# ---------------------------
# FILE UPLOAD
# ---------------------------
uploaded_file = st.file_uploader("📂 Upload your expense CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data.csv")

# ---------------------------
# DATA CLEANING
# ---------------------------
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
df = df.dropna()

# ---------------------------
# METRICS
# ---------------------------
total = df["Amount"].sum()
avg = df["Amount"].mean()

col1, col2 = st.columns(2)
col1.metric("💸 Total Spending", f"₹{round(total,2)}")
col2.metric("📊 Average Spending", f"₹{round(avg,2)}")

# ---------------------------
# CATEGORY ANALYSIS
# ---------------------------
st.subheader("📊 Category Analysis")

cat = df.groupby("Category")["Amount"].sum()

fig, ax = plt.subplots()
cat.plot(kind="bar", ax=ax)
st.pyplot(fig)

# ---------------------------
# TREND ANALYSIS
# ---------------------------
st.subheader("📈 Spending Trend")

df_sorted = df.sort_values("Date")

fig2, ax2 = plt.subplots()
ax2.plot(df_sorted["Date"], df_sorted["Amount"], marker='o')
plt.xticks(rotation=45)
st.pyplot(fig2)

# ---------------------------
# ANOMALY DETECTION
# ---------------------------
st.subheader("🚨 Anomaly Detection")

threshold = avg * 1.5
anomalies = df[df["Amount"] > threshold]

if not anomalies.empty:
    st.error("Unusual high spending detected")
    st.write(anomalies)
else:
    st.success("No anomalies detected")

# ---------------------------
# USER PERCEPTION
# ---------------------------
st.subheader("🧠 Your Perception")

perception = st.slider("Rate your spending (1-10)", 1, 10, 5)

# ---------------------------
# BEHAVIOR ANALYSIS
# ---------------------------
st.subheader("🧬 Behavioral Analysis")

top_cat = cat.idxmax()
st.info(f"You spend most on: {top_cat}")

# ---------------------------
# RISK SCORE
# ---------------------------
st.subheader("⚠️ Risk Score")

risk = 0

if total > avg:
    risk += 40
if len(anomalies) > 2:
    risk += 30
if perception > 7:
    risk += 30

st.metric("Risk Score", f"{risk}/100")

# ---------------------------
# AI INSIGHTS
# ---------------------------
st.subheader("🤖 AI Insights")

if risk > 70:
    st.error("🚨 High Risk: Overspending + unstable behavior")
elif risk > 40:
    st.warning("⚠ Moderate Risk: Monitor spending")
else:
    st.success("✅ Good financial control")

# ---------------------------
# PERCEPTION VS REALITY
# ---------------------------
st.subheader("⚖️ Perception vs Reality")

if perception > 7 and total > avg:
    st.warning("You think spending is fine, but actually high")
elif perception < 4 and total < avg:
    st.info("You are over-worrying about spending")
else:
    st.success("Perception matches reality")

# ---------------------------
# PREDICTION
# ---------------------------
st.subheader("🔮 Prediction")

pred = avg * 1.1
st.write(f"Next expected spending: ₹{round(pred,2)}")

# ---------------------------
# PDF REPORT
# ---------------------------
def create_pdf():
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph(f"Total Spending: ₹{total}", styles["Normal"]))
    content.append(Paragraph(f"Average Spending: ₹{avg}", styles["Normal"]))
    content.append(Paragraph(f"Risk Score: {risk}/100", styles["Normal"]))
    content.append(Paragraph(f"Top Category: {top_cat}", styles["Normal"]))

    doc.build(content)

create_pdf()

with open("report.pdf", "rb") as f:
    st.download_button("📄 Download Report", f, file_name="finance_report.pdf")

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.markdown("🚀 Developed by Dhivya M S | AI Finance PRO")
