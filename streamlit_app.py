import streamlit as st
import pandas as pd
import random

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Electrolysis AI Tutor v7.1", layout="wide")

# -------------------------
# LOAD QUESTIONS
# -------------------------
df = pd.read_csv("questions.csv")

# -------------------------
# SESSION STATE
# -------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "level" not in st.session_state:
    st.session_state.level = 1
if "lives" not in st.session_state:
    st.session_state.lives = 3
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "qa_order" not in st.session_state:
    st.session_state.qa_order = []
if "completed_lab" not in st.session_state:
    st.session_state.completed_lab = False
if "answered_questions" not in st.session_state:
    st.session_state.answered_questions = {}

# -------------------------
# SIDEBAR PROFILE
# -------------------------
st.sidebar.title("Student Profile")
name = st.sidebar.text_input("Enter Your Name", "")
st.sidebar.write("Score:", st.session_state.score)
st.sidebar.write("Level:", st.session_state.level)
st.sidebar.write("Lives:", st.session_state.lives)

# Badges
badges = []
if st.session_state.score >= 50:
    badges.append("Bronze")
if st.session_state.score >= 100:
    badges.append("Silver")
if st.session_state.score >= 150:
    badges.append("Gold")
st.sidebar.write("Badges:", badges)

# -------------------------
# FUNCTIONS
# -------------------------
def get_lab_questions():
    return df[df["level"] == 1].to_dict("records")

def get_level_questions(level, num_questions=10):
    qs = df[(df["level"] == level) & (df["type"] == "yaq")].sample(n=num_questions)
    return qs.to_dict("records")

def reset_level():
    st.session_state.question_index = 0
    st.session_state.answered_questions = {}
    if st.session_state.level == 2:
        st.session_state.qa_order = get_level_questions(2)
    elif st.session_state.level == 3:
        st.session_state.qa_order = get_level_questions(3)
    else:
        st.session_state.qa_order = []

# -------------------------
# LEVEL 1 - LAB (Drag and Drop)
# -------------------------
if st.session_state.level == 1:
    st.title("⚡ Electrolysis Lab - Drag and Drop")
    lab_qs = get_lab_questions()
    for q in lab_qs:
        st.subheader(q["topic"])
        st.write(q["question"])
        # Simulate drag and drop by selectbox for mobile
        user_choice = st.selectbox("Select the correct item to drag:", [q["option1"], q["option2"], q["option3"], q["option4"]], key=q["question"])
        if st.button(f"Submit: {q['question']}", key="submit_"+q["question"]):
            if user_choice == q["answer"]:
                st.success("Correct!")
                st.session_state.score += 10
            else:
                st.error("Wrong! Try again.")
                st.session_state.lives -= 1
    if st.button("Complete Lab"):
        st.session_state.completed_lab = True
        st.session_state.level = 2
        reset_level()
        st.experimental_rerun()

# -------------------------
# LEVEL 2 & 3 - QUIZ
# -------------------------
elif st.session_state.level in [2, 3]:
    st.title(f"⚡ Electrolysis Quiz - Level {st.session_state.level}")
    
    # Load questions for level
    if not st.session_state.qa_order:
        reset_level()
    
    if st.session_state.question_index < len(st.session_state.qa_order):
        q = st.session_state.qa_order[st.session_state.question_index]
        st.subheader(f"Question {st.session_state.question_index + 1} of {len(st.session_state.qa_order)}")
        st.write(q["question"])
        
        # Show options
        user_choice = st.radio("Choose your answer:", [q["option1"], q["option2"], q["option3"], q["option4"]], key=q["question"])
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            if st.button("Previous"):
                if st.session_state.question_index > 0:
                    st.session_state.question_index -= 1
                    st.experimental_rerun()
        with col2:
            if st.button("Submit"):
                if user_choice == q["answer"]:
                    st.success("Correct!")
                    if st.session_state.question_index not in st.session_state.answered_questions:
                        st.session_state.score += 5
                    st.session_state.answered_questions[st.session_state.question_index] = True
                else:
                    st.error(f"Wrong! Correct answer: {q['answer']}")
                    st.session_state.lives -= 1
                    st.session_state.answered_questions[st.session_state.question_index] = False
        with col3:
            if st.button("Next"):
                if st.session_state.question_index < len(st.session_state.qa_order) - 1:
                    st.session_state.question_index += 1
                    st.experimental_rerun()
                else:
                    st.success("You have reached the end of this level!")
                    if st.session_state.level == 2:
                        st.session_state.level = 3
                        reset_level()
                        st.experimental_rerun()
    else:
        st.write("No more questions in this level!")

# -------------------------
# GAME OVER CONDITION
# -------------------------
if st.session_state.lives <= 0:
    st.error("Game Over! You have no more lives.")
    if st.button("Restart Game"):
        st.session_state.level = 1
        st.session_state.score = 0
        st.session_state.lives = 3
        st.session_state.completed_lab = False
        reset_level()
        st.experimental_rerun()
