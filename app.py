import streamlit as st
import pandas as pd
import random

if "session_questions" not in st.session_state:
    st.session_state.session_questions = []

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

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
def why_interviewers_ask(row):
    domain = row["Domain"]
    sub = row["Subdomain"]

    return (
        f"This question is asked to evaluate your understanding of {sub} "
        f"and how well you can apply {domain} concepts to real-world problems."
    )


#UI
st.set_page_config(page_title="AI Interview Qestion Generator", layout= "centered")
st.title("AI Interview Question Generator")
st.caption("Smart -Adaptive -Zero Paid APIs")
domains = sorted(data["Domain"].unique())
question_types = ["Theory", "Scenario", "MCQ", "Coding"]

domain = st.selectbox("Choose Domain", domains)
qtype = st.selectbox("Question Type", question_types)

if st.button("Start Practice Session"):
    st.session_state.session_questions = (
        fetch_question(domain, 5).reset_index(drop=True)
    )
    st.session_state.current_index = 0

if st.session_state.session_questions != []:
    idx = st.session_state.current_index
    questions = st.session_state.session_questions

    if idx < len(questions):
        row = questions.iloc[idx]

        st.subheader(f"Question {idx + 1}")
        st.write(transform_question(row["Question"], qtype))

        with st.expander("Show Answer"):
            st.write(better_answer(row))

        with st.expander("Why interviewers ask this"):
            st.write(why_interviewers_ask(row))

        if st.button("Next Question"):
            st.session_state.current_index += 1
    else:
        st.success("Practice session completed!")
