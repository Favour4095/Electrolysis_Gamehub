import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Electrolysis AI Tutor – Level Game", layout="wide")
st.title("⚡ Electrolysis AI Tutor – Level Game")

# --- SESSION STATE ---
if "level" not in st.session_state: st.session_state.level = 1
if "score" not in st.session_state: st.session_state.score = 0
if "lives" not in st.session_state: st.session_state.lives = 3
if "xp" not in st.session_state: st.session_state.xp = 0
if "stars" not in st.session_state: st.session_state.stars = 0
if "streak" not in st.session_state: st.session_state.streak = 0
if "question_index" not in st.session_state: st.session_state.question_index = 0
if "answers" not in st.session_state: st.session_state.answers = []
if "question_history" not in st.session_state: st.session_state.question_history = []

# --- LOAD QUESTIONS ---
questions_df = pd.read_csv("Questions.csv")  # question bank for YAQ and labs
questions_df = questions_df.sample(frac=1).reset_index(drop=True)  # shuffle for random order

# --- PLAYER PANEL ---
st.sidebar.title("Player")
st.sidebar.metric("Level", st.session_state.level)
st.sidebar.metric("Score", st.session_state.score)
st.sidebar.metric("Lives ❤️", st.session_state.lives)
st.sidebar.metric("XP ⚡", st.session_state.xp)
st.sidebar.metric("Stars ⭐", st.session_state.stars)

# --- FUNCTION TO DISPLAY QUESTION ---
def display_question(index):
    q = questions_df.iloc[index]
    st.subheader(f"Question {index+1}")
    st.write(f"Topic: {q['topic']}")
    st.write(q["question"])
    choice = st.radio("Select Answer", [q["option1"], q["option2"], q["option3"], q["option4"]],
                      key=f"question_{index}")
    return choice

# --- CURRENT QUESTION ---
current_index = st.session_state.question_index
choice = display_question(current_index)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Previous"):
        if st.session_state.question_index > 0:
            st.session_state.question_index -= 1
            st.rerun()

with col2:
    if st.button("Submit"):
        q = questions_df.iloc[current_index]
        if choice == q["answer"]:
            st.success("Correct!")
            st.session_state.score += 10
            st.session_state.xp += 10
            st.session_state.streak += 1
            st.session_state.stars += 1
        else:
            st.error(f"Wrong! Hint: {q['topic']}")
            st.session_state.lives -= 1
            st.session_state.streak = 0

        # Save answer in history
        if len(st.session_state.answers) > current_index:
            st.session_state.answers[current_index] = choice
        else:
            st.session_state.answers.append(choice)
        st.session_state.question_history.append(current_index)

with col3:
    if st.button("Next"):
        if current_index + 1 < len(questions_df):
            st.session_state.question_index += 1
            st.rerun()
        else:
            st.success("End of level!")

# --- LEVEL COMPLETION CHECK ---
if st.session_state.score >= 50:  # threshold to pass level
    st.balloons()
    st.success(f"Level {st.session_state.level} Complete! 🎉")
    st.session_state.level += 1
    st.session_state.score = 0
    st.session_state.question_index = 0
    st.session_state.answers = []
    st.rerun()

# --- GAME OVER ---
if st.session_state.lives <= 0:
    st.error("Game Over! 😢")
    if st.button("Restart Game"):
        st.session_state.level = 1
        st.session_state.score = 0
        st.session_state.lives = 3
        st.session_state.xp = 0
        st.session_state.stars = 0
        st.session_state.streak = 0
        st.session_state.question_index = 0
        st.session_state.answers = []
        st.session_state.question_history = []
        st.rerun()
