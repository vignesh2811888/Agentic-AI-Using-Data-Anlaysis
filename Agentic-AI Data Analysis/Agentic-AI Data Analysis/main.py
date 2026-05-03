import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import pdfplumber
import io
import speech_recognition as sr

from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password TEXT
)
""")
conn.commit()


def add_user(email, password):
    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (email, password))
        conn.commit()
        return True
    except:
        return False


def login_user(email, password):
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    return c.fetchone()


# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Agentic AI Data Analyst", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1f1c2c, #928dab);
    color: white;
}
.stButton>button {
    border-radius: 10px;
    background: #ff4b2b;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- USERS ----------------
users = {"admin@gmail.com": "1234"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "signup_mode" not in st.session_state:
    st.session_state.signup_mode = False

# ---------------- LOGIN / SIGNUP ----------------
if not st.session_state.logged_in:
    st.title("🔐 Login / Sign Up")

    if st.button("Switch Mode"):
        st.session_state.signup_mode = not st.session_state.signup_mode

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # -------- SIGNUP --------
    if st.session_state.signup_mode:
        if st.button("Create Account"):
            if add_user(email, password):
                st.success("Account created successfully!")
            else:
                st.error("User already exists!")

    # -------- LOGIN --------
    else:
        if st.button("Login"):
            if login_user(email, password):
                st.session_state.logged_in = True
                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Invalid Credentials")

    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🤖 AI Data Analyst")

theme = st.sidebar.radio("Theme", ["Dark", "Light"])

if theme == "Light":
    st.markdown("<style>.stApp{background:white;color:black;}</style>", unsafe_allow_html=True)

menu = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Upload & Analyze", "Compare Files", "Chat", "History", "Logout"]
)

# ---------------- LOGOUT ----------------
if menu == "Logout":
    st.session_state.logged_in = False
    st.rerun()


# ---------------- LLM ----------------
def ask_llm(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "tinyllama", "prompt": prompt, "stream": False},
            timeout=120
        )
        return response.json()["response"]
    except:
        return "⚠️ Ollama not running"


# ---------------- PDF ----------------
def generate_pdf(text):
    file_path = "report.pdf"
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    story = [Paragraph(line, styles["Normal"]) for line in text.split("\n")]
    doc.build(story)
    return file_path


# ---------------- SESSION ----------------
if "history" not in st.session_state:
    st.session_state.history = []
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- HOME ----------------
if menu == "Home":

    # -------- HERO SECTION --------
    st.markdown("""
    <div style='text-align:center; padding:40px'>
        <h1 style='font-size:50px;'>🧠 Agentic AI Data Analyst</h1>
        <p style='font-size:20px;'>Analyze • Predict • Chat • Automate</p>
    </div>
    """, unsafe_allow_html=True)

    # -------- FEATURE CARDS --------
    st.markdown("### 🚀 Key Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style='padding:20px; border-radius:15px; background:#262730'>
        📊 <b>Smart Data Analysis</b><br>
        Automatic insights, charts & KPIs
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='padding:20px; border-radius:15px; background:#262730'>
        🤖 <b>AI Chat Assistant</b><br>
        Ask questions about your data
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style='padding:20px; border-radius:15px; background:#262730'>
        🔮 <b>ML Predictions</b><br>
        Predict future values instantly
        </div>
        """, unsafe_allow_html=True)

    # -------- HOW IT WORKS --------
    st.markdown("### ⚙️ How It Works")

    st.markdown("""
    1️⃣ Upload Dataset / PDF  
    2️⃣ Get Instant Insights  
    3️⃣ Chat with AI  
    4️⃣ Download Reports  
    """)

    # -------- LIVE METRICS --------
    st.markdown("### 📊 Live System Stats")

    col1, col2, col3 = st.columns(3)

    col1.metric("Users", "120+")
    col2.metric("Files Analyzed", "500+")
    col3.metric("Predictions Made", "1.2K+")

    # -------- CTA BUTTON --------
    st.markdown("### 🚀 Get Started")

    if st.button("Go to Upload Page"):
        st.session_state.page = "Upload & Analyze"
        st.success("Use sidebar to navigate → Upload & Analyze")

    # -------- ANIMATION (LOTTIE STYLE SIMULATION) --------
    st.markdown("""
    <div style='text-align:center; font-size:60px; animation: pulse 2s infinite;'>
    📈
    </div>

    <style>
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- UPLOAD ----------------
elif menu == "Upload & Analyze":

    file = st.file_uploader("Upload CSV/Excel/PDF", type=["csv", "xlsx", "pdf"])

    if file:
        st.session_state.history.append(file.name)
        file_type = file.name.split(".")[-1]

        # ---------- CSV ----------
        if file_type in ["csv", "xlsx"]:
            df = pd.read_csv(file) if file_type == "csv" else pd.read_excel(file)

            st.session_state.df = df

            st.subheader("Preview")
            st.dataframe(df.head())

            # KPI
            c1, c2, c3 = st.columns(3)
            c1.metric("Rows", df.shape[0])
            c2.metric("Columns", df.shape[1])
            c3.metric("Missing", df.isnull().sum().sum())

            # Preprocess
            df = df.drop_duplicates()
            for col in df.columns:
                if df[col].dtype == "object":
                    df[col].fillna("Unknown", inplace=True)
                else:
                    df[col].fillna(df[col].mean(), inplace=True)

            le = LabelEncoder()
            for col in df.columns:
                if df[col].dtype == "object":
                    df[col] = le.fit_transform(df[col])

            st.write(df.describe())

            numeric = df.select_dtypes(include="number").columns

            # Charts
            for col in numeric[:3]:
                fig, ax = plt.subplots()
                sns.histplot(df[col], kde=True)
                st.pyplot(fig)

            if len(numeric) > 1:
                fig, ax = plt.subplots()
                sns.heatmap(df[numeric].corr(), annot=True)
                st.pyplot(fig)

            # Advanced
            if len(numeric) >= 2:
                fig, ax = plt.subplots()
                sns.scatterplot(x=df[numeric[0]], y=df[numeric[1]])
                st.pyplot(fig)

            # Prediction
            if len(numeric) >= 2:
                X = df[numeric[:-1]]
                y = df[numeric[-1]]

                models = {
                    "Linear": LinearRegression(),
                    "Tree": DecisionTreeRegressor(),
                    "Forest": RandomForestRegressor()
                }

                for name, m in models.items():
                    m.fit(X, y)
                    pred = m.predict([X.iloc[-1]])
                    st.write(name, ":", float(pred[0]))

            # AI Insights
            st.write(ask_llm(str(df.describe())))

            # Download txt
            report = str(df.describe())
            st.download_button("Download Report", report)

            # PDF
            if st.button("Download PDF"):
                path = generate_pdf(report)
                with open(path, "rb") as f:
                    st.download_button("Download", f)

        # ---------- PDF ----------
        elif file_type == "pdf":
            text = ""
            with pdfplumber.open(file) as pdf:
                for p in pdf.pages:
                    if p.extract_text():
                        text += p.extract_text()

            st.session_state.pdf_text = text
            st.write(text[:1000])
            st.write(ask_llm(text[:2000]))

# ---------------- COMPARE ----------------
elif menu == "Compare Files":

    st.header("📂 Compare Two Files")

    file1 = st.file_uploader("Upload First File", key="f1")
    file2 = st.file_uploader("Upload Second File", key="f2")

    if file1 and file2:
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)

        # ---------------- DATASET SIZE ----------------
        st.subheader("📊 Dataset Size")

        col1, col2 = st.columns(2)

        with col1:
            st.write("File 1 Shape")
            st.write(df1.shape)

        with col2:
            st.write("File 2 Shape")
            st.write(df2.shape)

        # ---------------- COLUMN COMPARISON ----------------
        st.subheader("📌 Column Comparison")

        st.write("Common Columns:", list(set(df1.columns) & set(df2.columns)))
        st.write("Only in File1:", list(set(df1.columns) - set(df2.columns)))
        st.write("Only in File2:", list(set(df2.columns) - set(df1.columns)))

        # ---------------- SUMMARY ----------------
        st.subheader("📈 Summary Statistics")

        st.write("File 1 Summary")
        st.write(df1.describe())

        st.write("File 2 Summary")
        st.write(df2.describe())

# ---------------- CHAT ----------------
elif menu == "Chat":

    st.header("💬 Chat with Data")

    user_input = st.chat_input("Ask something...")

    if user_input:

        st.session_state.messages.append({"role": "user", "content": user_input})

        # -------- CONTEXT --------
        if "df" in st.session_state:
            context = st.session_state.df.describe().to_string()

            prompt = f"""
Dataset Summary:
{context}

User Question:
{user_input}

Answer clearly.
"""

        elif "pdf_text" in st.session_state:
            prompt = f"""
Document:
{st.session_state.pdf_text[:2000]}

Question:
{user_input}
"""

        else:
            prompt = user_input

        response = ask_llm(prompt)

        st.session_state.messages.append({"role": "assistant", "content": response})

    # -------- DISPLAY CHAT --------
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
        # -------- CONTEXT HANDLING --------
        if "df" in st.session_state:
            context = st.session_state.df.describe().to_string()

            prompt = f"""
Dataset Summary:
{context}

User Question:
{user_input}

Give a clear answer.
"""

        elif "pdf_text" in st.session_state:
            prompt = f"""
Document:
{st.session_state.pdf_text[:2000]}

Question:
{user_input}
"""

        else:
            prompt = user_input

        # -------- AI RESPONSE --------
        response = ask_llm(prompt)

        # Store response
        st.session_state.messages.append({"role": "assistant", "content": response})

    # ---------------- DISPLAY CHAT ----------------
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# ---------------- HISTORY ----------------
elif menu == "History":
    for f in st.session_state.history:
        st.write(f)