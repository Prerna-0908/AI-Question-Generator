import streamlit as st
import pandas as pd
import random
@st.cache_data
def load_data():
    data = pd.read_csv("interview_questions.csv")
    data["Asked_Count"] = 0
    return data

data = load_data()

#logic Function
def fetch_question(domain, n=1):
    subset = data[data["Domain"] ==domain].copy()
    if subset.empty:
        return None
    subset["weight"] = 1 / (subset["Asked_Count"] + 1)
    selected = subset.sample(n=min(n,len(subset)),weights= subset["weight"])
    data.loc[selected.index,"Asked_Count"] +=1
    return selected

def transform_question(question, qtype):
    if qtype == "Scenario":
        return f"Scenario Based: {question}\nExplain how wold yo handle this in real world."
    elif type == "MCQ":
        return f"{question} (Choose the correct option)"
    elif type == "Coding":
        return f"Write code to: {question}"
    else:
        return question

def infer_difficulty(subdomain):
    easy = ["Basics", "EDA", "Probability"]
    medium = ["Joins", "Regression", "Tokenization"]

    if subdomain in easy:
        return "Beginner"
    elif subdomain in medium:
        return "Intermediate"
    else:
        return "Advanced"

def better_answer(row):
    return f"""
**What it is:**  
{row['Answer']}

**Why it matters:**  
This topic is important because it is commonly used in real-world applications and frequently asked in interviews.

**Where it is used:**  
Used in practical systems related to {row['Domain']}.

**Interview tip:**  
Be clear with the definition and give one real-world example.
"""

#UI
st.set_page_config(page_title="AI Interview Qestion Generator", layout= "centered")
st.title("AI Interview Question Generator")
st.caption("Smart -Adaptive -Zero Paid APIs")
domains = sorted(data["Domain"].unique())
question_types = ["Theory", "Scenario", "MCQ", "Coding"]

domain = st.selectbox("Choose Domain", domains)
qtype = st.selectbox("Question Type", question_types)

if st.button("Generate Question"):
    result = fetch_question(domain, 1)
    if result is not None:
        row = result.iloc[0]
        st.subheader("Question")
        st.write(transform_question(row["Question"], type))
        with st.expander("Show Answer"):
            st.write(better_answer(row))
        difficulty = infer_difficulty(row["Subdomain"])    
        st.caption(f"Difficulty: **{'Difficulty'}**")
