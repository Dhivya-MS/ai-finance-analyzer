import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Finance Analyzer", layout="wide")

# =========================
# 🔐 LOGIN
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == "admin" and p == "1234":
            st.session_state.logged_in = True
            st.success("Login success")
            st.rerun()
        else:
            st.error("Wrong credentials")

    st.stop()

if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# =========================
# TITLE
# =========================
st.title("💰 AI Financial Analyzer")

# =========================
# STORAGE
# =========================
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# =========================
# MODE
# =========================
mode = st.radio("Choose 👇", ["Upload CSV", "Manual Entry"])

# =========================
# CSV
# =========================
if mode == "Upload CSV":
    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.session_state.df = df
    else:
        st.warning("Upload file")
        st.stop()

# =========================
# MANUAL
# =========================
if mode == "Manual Entry":

    date = st.date_input("Date")

    cat_opt = st.selectbox("Category", ["Food","Travel","Shopping","Bills","Others"])

    if cat_opt == "Others":
        custom = st.text_input("Enter category")
        category = custom if custom else "Others"
    else:
        category = cat_opt

    amount = st.number_input("Amount", min_value=0.0)

    if st.button("Add"):
        st.session_state.expenses.append({
            "Date": str(date),
            "Category": category,
            "Amount": amount
        })
        st.success("Added")

    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        st.session_state.df = df

# =========================
# CHECK
# =========================
if "df" not in st.session_state:
    st.warning("Add data")
    st.stop()

df = st.session_state.df

# =========================
# FIX TYPES
# =========================
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
df = df.dropna(subset=["Amount"])

# =========================
# SHOW DATA
# =========================
st.subheader("📊 Data")
st.dataframe(df)

# =========================
# SUMMARY
# =========================
total = df["Amount"].sum()
avg = df["Amount"].mean()

st.subheader("💰 Summary")
st.write(f"Total: ₹{total:.2f}")
st.write(f"Average: ₹{avg:.2f}")

# =========================
# CATEGORY GRAPH
# =========================
cat = df.groupby("Category")["Amount"].sum()

st.subheader("📊 Category Bar")
fig, ax = plt.subplots()
cat.plot(kind="bar", ax=ax)
st.pyplot(fig)

# =========================
# PIE
# =========================
st.subheader("🥧 Pie")
fig2, ax2 = plt.subplots()
cat.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
ax2.set_ylabel("")
st.pyplot(fig2)

# =========================
# MONTHLY
# =========================
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Month"] = df["Date"].dt.to_period("M")

monthly = df.groupby("Month")["Amount"].sum()

st.subheader("📅 Monthly Spending")
fig3, ax3 = plt.subplots()
monthly.plot(kind="bar", ax=ax3)
st.pyplot(fig3)

# =========================
# PREDICTION
# =========================
st.subheader("🔮 Prediction")

if len(monthly) >= 2:
    pred = monthly.mean()
    st.info(f"👉 Next month approx spend: ₹{pred:.2f}")
else:
    st.warning("Need more data")

# =========================
# DELETE
# =========================
st.subheader("❌ Delete")

i = st.number_input("Index", min_value=0, step=1)

if st.button("Delete"):
    if mode == "Manual Entry" and i < len(st.session_state.expenses):
        st.session_state.expenses.pop(i)
        st.session_state.df = pd.DataFrame(st.session_state.expenses)
        st.success("Deleted")
        st.rerun()
    else:
        st.error("Invalid")

# =========================
# DOWNLOAD
# =========================
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv)

# =========================
# AI INSIGHT
# =========================
st.subheader("🤖 AI Insight")

if total > 5000:
    st.warning("High spending")
else:
    st.success("Good control")

# =========================
# ADVICE
# =========================
top = cat.idxmax()
st.subheader("🎯 Advice")
st.info(f"Reduce spending on {top}")
