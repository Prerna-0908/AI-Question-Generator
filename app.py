import streamlit as st
import pandas as pd
import random
@st.cache_data
def load_data():
    data = pd.read_csv("interview_questions")
    data["Asked_Count"] = 0
    return data

data =load_data()

#logic Function
def fetch_question(domain, n=1):
    suubset = data[data["Domain"] ==domain].copy()
    subset["weight"] = 1 / (subset["Asked_Count"] + 1)
    selected = subset.sample(n=min(n,len(subset)),weights= subset["weight"])
    data.loc[selected.index,"Asked_Count"] +=1
    return selected

def transform_qestion(question, type):
    if qtype == "Scenario":
        return f"Scenario Based: {question} Explain how wold yo handle this in real world."
    elif type == "MCQ":
        return f"{question} (Choose the correct option)"
    elif type == "Coding":
        return f"Write code to: {question}"
    else:
        return question

#UI
st.set_page_config(page_title="AI Interview Qestion Generator", layout= "centered")
st.title("AI Interview Question Generator")
st.caption("Smart -Adaptive -Zero PAid APIs")
domains = sorted(data["Domain"].unique())
question_types = ["Theory", "Scenario", "MCQ", "Coding"]

domain = st.selectbox("Choose Domain", domains)
qtype = st.selectbox("Question Type", question_types)

if st.button("Generate Question"):
    row = fetch_questions(domain, 1).iloc[0]

    st.subheader("Question")
    st.write(transform_question(row["Question"], qtype))

    with st.expander("Show Answer"):
        st.write(row["Answer"])

    st.caption(f"Difficulty: **{row['Difficulty']}**")
    
