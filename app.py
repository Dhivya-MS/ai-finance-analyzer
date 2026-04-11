import streamlit as st
import pandas as pd

# ---------------------------
# SESSION INIT
# ---------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "expenses" not in st.session_state:
    st.session_state.expenses = []

# ---------------------------
# LOGIN PAGE
# ---------------------------
if not st.session_state.logged_in:
    st.title("🔐 Login to AI Finance Analyzer")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login successful ✅")
            st.rerun()   # 🔥 IMPORTANT
        else:
            st.error("Invalid credentials ❌")

    st.stop()

# ---------------------------
# MAIN APP (AFTER LOGIN)
# ---------------------------
st.title("💰 AI-Based Financial Risk & Behavior Analyzer")
st.markdown("### 🔍 Smart AI insights into your spending")

# LOGOUT
if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ---------------------------
# MODE SELECT
# ---------------------------
mode = st.radio("Choose how you want to use the app 👇", ["Upload CSV", "Manual Entry"])

# ---------------------------
# UPLOAD CSV
# ---------------------------
if mode == "Upload CSV":
    uploaded_file = st.file_uploader("📁 Upload your expense CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
    else:
        st.warning("Please upload a CSV file")
        st.stop()

# ---------------------------
# MANUAL ENTRY
# ---------------------------
if mode == "Manual Entry":
    st.subheader("➕ Add Expense Manually")

    date = st.date_input("Select Date")
    category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Others"])
    amount = st.number_input("Amount", min_value=0.0)

    if st.button("Add Expense"):
        st.session_state.expenses.append({
            "Date": str(date),
            "Category": category,
            "Amount": amount
        })
        st.success("Expense added!")

    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        st.session_state.df = df

# ---------------------------
# CHECK DATA
# ---------------------------
if "df" not in st.session_state:
    st.warning("Please add or upload data to continue")
    st.stop()

df = st.session_state.df

# ---------------------------
# DISPLAY DATA
# ---------------------------
st.write("### 📊 Your Data")
st.dataframe(df)

# ---------------------------
# ANALYSIS
# ---------------------------
st.write("### 📈 Analysis")

total = df["Amount"].sum()
avg = df["Amount"].mean()

st.write(f"💸 Total Spending: ₹{total}")
st.write(f"📊 Average Spending: ₹{round(avg,2)}")

# ---------------------------
# CATEGORY CHART
# ---------------------------
st.write("### 🧾 Category Breakdown")
cat = df.groupby("Category")["Amount"].sum()
st.bar_chart(cat)

# ---------------------------
# DELETE OPTION
# ---------------------------
st.write("### ❌ Delete Expense")

delete_index = st.number_input("Enter index to delete", min_value=0, step=1)

if st.button("Delete"):
    if mode == "Manual Entry" and 0 <= delete_index < len(st.session_state.expenses):
        st.session_state.expenses.pop(delete_index)
        st.success("Deleted successfully")
    else:
        st.error("Invalid index or CSV mode")

# ---------------------------
# DOWNLOAD
# ---------------------------
st.write("### 💾 Download Data")

csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="expenses.csv",
    mime="text/csv"
)

# ---------------------------
# AI INSIGHT
# ---------------------------
st.write("### 🤖 AI Insight")

if total > 5000:
    st.warning("⚠️ High spending! Reduce expenses.")
elif total > 2000:
    st.info("🙂 Moderate spending.")
else:
    st.success("🔥 Good financial control!")

# ---------------------------
# ADVICE
# ---------------------------
st.write("### 🎯 Advice")

highest = df.groupby("Category")["Amount"].sum().idxmax()
st.write(f"👉 You spend most on **{highest}**. Try to reduce it!")
