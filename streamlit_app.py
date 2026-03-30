import streamlit as st
import pandas as pd
import random
import sqlite3

st.set_page_config(page_title="Electrolysis AI Tutor v7.2", layout="wide")

# -------------------------
# LOAD QUESTIONS
# -------------------------
df = pd.read_csv("electrolysis_questions.csv")  # Use the CSV we just generated

# -------------------------
# DATABASE
# -------------------------
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    name TEXT,
    score INTEGER,
    accuracy REAL,
    level INTEGER
)
""")
conn.commit()

# -------------------------
# SESSION STATE
# -------------------------
if "score" not in st.session_state: st.session_state.score = 0
if "level" not in st.session_state: st.session_state.level = 1
if "mistakes" not in st.session_state: st.session_state.mistakes = 0
if "correct" not in st.session_state: st.session_state.correct = 0
if "name" not in st.session_state: st.session_state.name = ""
if "question_index" not in st.session_state: st.session_state.question_index = 0
if "question_order" not in st.session_state: st.session_state.question_order = []
if "current_question" not in st.session_state: st.session_state.current_question = None
if "lives" not in st.session_state: st.session_state.lives = 3  # For lab drag-and-drop

# -------------------------
# STUDENT PROFILE SIDEBAR
# -------------------------
st.sidebar.title("Student Profile")
name = st.sidebar.text_input("Student Name")
st.session_state.name = name
st.sidebar.write("Score:", st.session_state.score)
st.sidebar.write("Level:", st.session_state.level)
st.sidebar.write("Lives:", st.session_state.lives)

# Badges
badges = []
if st.session_state.score >= 50: badges.append("Bronze")
if st.session_state.score >= 100: badges.append("Silver")
if st.session_state.score >= 150: badges.append("Gold")
st.sidebar.write("Badges:", badges)

# -------------------------
# FUNCTIONS
# -------------------------
def load_questions(level):
    subset = df[df["level"] == level].reset_index(drop=True)
    return subset

def next_question():
    if st.session_state.question_index < len(st.session_state.question_order)-1:
        st.session_state.question_index += 1
        st.session_state.current_question = st.session_state.question_order[st.session_state.question_index]

def previous_question():
    if st.session_state.question_index > 0:
        st.session_state.question_index -= 1
        st.session_state.current_question = st.session_state.question_order[st.session_state.question_index]

def reset_level():
    st.session_state.score = 0
    st.session_state.correct = 0
    st.session_state.mistakes = 0
    st.session_state.lives = 3
    st.session_state.question_index = 0
    st.session_state.question_order = load_questions(st.session_state.level).to_dict('records')
    st.session_state.current_question = st.session_state.question_order[0]

# -------------------------
# INITIALIZE QUESTIONS
# -------------------------
if st.session_state.current_question is None or st.session_state.level_changed:
    st.session_state.question_order = load_questions(st.session_state.level).to_dict('records')
    random.shuffle(st.session_state.question_order)
    st.session_state.current_question = st.session_state.question_order[0]
    st.session_state.question_index = 0
    st.session_state.level_changed = False

q = st.session_state.current_question

# -------------------------
# MAIN GAME INTERFACE
# -------------------------
st.title("⚡ AI Electrolysis WAEC Learning Game")

st.subheader(f"Level {st.session_state.level} - {q['topic']}")

# Level 1: Drag-and-Drop style lab
if st.session_state.level == 1:
    st.write(q["question"])
    # Create drag options for lab
    options = ["H+", "Cl-", "Cu2+", "O2", "Na+", "OH-"]  # Example items for drag-and-drop
    selected_items = st.multiselect("Select ions to drag to electrode:", options)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit Answer"):
            correct_item = q["answer"]
            if correct_item in selected_items:
                st.success("Correct! 🎉")
                st.session_state.score += 10
                st.session_state.correct += 1
                st.balloons()
                next_question()
            else:
                st.error("Wrong! ❌")
                st.session_state.mistakes += 1
                st.session_state.lives -= 1
                st.info("Hint: " + q["hint"])
                if st.session_state.lives == 0:
                    st.warning("Game Over! No more lives left.")
                    reset_level()

    with col2:
        if st.button("Next Question"):
            next_question()

# Levels 2 & 3: WAEC-style quiz and Challenge
else:
    st.write(q["question"])
    choice = st.radio("Choose answer:", [q["option1"], q["option2"], q["option3"], q["option4"]])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit Answer"):
            if choice == q["answer"]:
                st.success("Correct! 🎉")
                st.session_state.score += 10
                st.session_state.correct += 1
                st.balloons()
                next_question()
            else:
                st.error("Wrong! ❌")
                st.session_state.mistakes += 1
                st.info("Hint: " + q["hint"])
                next_question()

    with col2:
        if st.button("Next Question"):
            next_question()

# Previous button
if st.button("Previous Question"):
    previous_question()

# -------------------------
# PROGRESS BAR & METRICS
# -------------------------
attempts = st.session_state.correct + st.session_state.mistakes
accuracy = 0
if attempts > 0:
    accuracy = (st.session_state.correct / attempts) * 100

st.progress(min(st.session_state.score / 150, 1.0))
st.subheader("AI Performance")
st.metric("Accuracy", round(accuracy, 1))

if accuracy < 50:
    st.error("AI Advice: Revise ion movement")
elif accuracy < 75:
    st.warning("AI Advice: Practice discharge")
else:
    st.success("AI Advice: Ready for exam")

# -------------------------
# SAVE PROGRESS
# -------------------------
if st.button("Save Progress"):
    cursor.execute("""
    INSERT INTO students VALUES(?,?,?,?)
    """, (st.session_state.name, st.session_state.score, accuracy, st.session_state.level))
    conn.commit()
    st.success("Progress Saved ✅")

# -------------------------
# TEACHER VIEW
# -------------------------
if st.checkbox("Teacher Dashboard"):
    data = cursor.execute("SELECT * FROM students").fetchall()
    st.write(data)

# -------------------------
# RESET
# -------------------------
if st.button("Restart Game"):
    st.session_state.level_changed = True
    reset_level()
    st.experimental_rerun()
