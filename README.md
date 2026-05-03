🧠 Agentic AI Data Analyst

A Streamlit-based AI-powered data analysis application that enables users to upload datasets or PDFs, generate insights, visualize data, run machine learning models, and interact with data through an AI chat interface.

🚀 Overview

This project combines:

📊 Data analysis
🤖 AI-powered insights (via local LLM)
🔮 Machine learning predictions
📄 PDF understanding
🔐 User authentication

All inside a single interactive web app.

✨ Features
🔐 Authentication System
User Sign Up & Login
SQLite database (users.db)
Session-based login handling
📊 Upload & Analyze Data
Supports:
CSV files
Excel files
Features:
Data preview
Automatic cleaning:
Remove duplicates
Fill missing values
Label encoding for categorical columns
Summary statistics
📈 Data Visualization
Histogram plots (first 3 numeric columns)
Correlation heatmap
Scatter plot (between numeric features)
🔮 Machine Learning Predictions

Automatically trains models on uploaded dataset:

Linear Regression
Decision Tree Regressor
Random Forest Regressor

➡️ Predicts value using last row of dataset

🤖 AI Insights (LLM Integration)

Uses local API:

http://localhost:11434/api/generate
Model: tinyllama
Generates:
Dataset insights
Answers to user questions
📄 PDF Analysis
Extracts text using pdfplumber
Displays content preview
AI-based summarization & Q&A
💬 Chat with Data
Ask questions about:
Uploaded dataset
Uploaded PDF
Context-aware responses using:
df.describe() for datasets
Extracted text for PDFs
📂 Compare Files
Upload two CSV files
Compare:
Dataset shape
Columns (common & unique)
Summary statistics
📜 Report Generation
Download:
Text report
PDF report (via reportlab)
🕓 History Tracking
Tracks uploaded file names in session
🛠️ Tech Stack
Category	Tools
UI	Streamlit
Data	Pandas, NumPy
Visualization	Matplotlib, Seaborn
ML	Scikit-learn
AI	Ollama (TinyLlama)
Database	SQLite
PDF	pdfplumber, reportlab
Voice	SpeechRecognition (imported)
📦 Installation
1. Clone Repository
git clone https://github.com/your-username/agentic-ai-data-analyst.git
cd agentic-ai-data-analyst
2. Install Dependencies
pip install -r requirements.txt
3. Start Ollama (Required for AI)
ollama run tinyllama

Make sure it's running at:

http://localhost:11434
4. Run the App
streamlit run app.py

Users can:

Create a new account
Login using stored credentials in SQLite


⚙️ How It Works
Login / Sign Up
Navigate using sidebar
Upload dataset or PDF
View insights & visualizations
Run ML predictions
Chat with AI
Download reports
