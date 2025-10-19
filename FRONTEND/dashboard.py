import streamlit as st
import json
import os
import sys

# ------------------- Fix for BACKEND imports -------------------
# Add BACKEND folder to Python path so we can import summarize.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'BACKEND')))

from summarize import summarize_text
# ---------------------------------------------------------------

# ------------------- Data folder path -------------------
# Dynamically get the path to the data folder
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# ------------------- Sidebar navigation -------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Headlines", "Deep Dive + Q&A", "Article Database"])

# ---------------- Headlines Page ----------------
if page == "Headlines":
    st.title("🗞️ Today's Headlines")
    # Load latest headlines file
    files = sorted([f for f in os.listdir(DATA_DIR) if f.startswith("headlines_")])
    if files:
        latest_file = os.path.join(DATA_DIR, files[-1])
        with open(latest_file) as f:
            headlines = json.load(f)
        for category, articles in headlines.items():
            st.subheader(category)
            for article in articles:
                st.markdown(f"- [{article['title']}]({article['link']})")
    else:
        st.info("No headlines found. Run the daily agent first.")

# ---------------- Deep Dive + Q&A Page ----------------
elif page == "Deep Dive + Q&A":
    st.title("🧠 Deep Dive")
    files = sorted([f for f in os.listdir(DATA_DIR) if f.startswith("deep_dive_")])
    if files:
        latest_file = os.path.join(DATA_DIR, files[-1])
        with open(latest_file) as f:
            deep_dive = json.load(f)
        st.subheader(deep_dive["headline"])
        st.markdown(f"[Source]({deep_dive['link']})")
        st.write("**Summary:**")
        st.write(deep_dive["summary"])

        st.subheader("Ask a question about this article")
        user_question = st.text_input("Enter your question here")
        if user_question:
            answer = summarize_text(f"{deep_dive['summary']}\nQuestion: {user_question}")
            st.write("**Answer:**")
            st.write(answer)
    else:
        st.info("No deep dive found. Run the daily agent first.")

# ---------------- Article Database Page ----------------
elif page == "Article Database":
    st.title("📚 Article Database")
    all_articles = []
    for file in os.listdir(DATA_DIR):
        if file.startswith("deep_dive_") or file.startswith("headlines_"):
            with open(os.path.join(DATA_DIR, file)) as f:
                data = json.load(f)
                if file.startswith("headlines_"):
                    for cat_articles in data.values():
                        all_articles.extend(cat_articles)
                else:
                    all_articles.append(data)
    if all_articles:
        import pandas as pd
        df = pd.DataFrame(all_articles)
        st.dataframe(df)
    else:
        st.info("No articles found. Run the daily agent first.")
