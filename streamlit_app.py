import streamlit as st
import pandas as pd
import random
import sqlite3

st.set_page_config(page_title="Electrolysis AI Tutor", layout="wide")

# -------------------------
# LOAD QUESTIONS
# -------------------------
df = pd.read_csv("questions.csv")

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
# SESSION STATE INITIALIZATION
# -------------------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "level" not in st.session_state:
    st.session_state.level = 1

if "mistakes" not in st.session_state:
    st.session_state.mistakes = 0

if "correct" not in st.session_state:
    st.session_state.correct = 0

if "name" not in st.session_state:
    st.session_state.name = ""

# FUNCTION TO GET QUESTION BY LEVEL
def get_question(level):
    subset = df[df["level"] == level]
    return subset.sample(1).iloc[0]

if "question" not in st.session_state:
    st.session_state.question = get_question(1)

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("Student Profile")
name = st.sidebar.text_input("Student Name")
st.session_state.name = name

st.sidebar.write("Score:", st.session_state.score)
st.sidebar.write("Level:", st.session_state.level)

# BADGES
badges = []
if st.session_state.score >= 50:
    badges.append("Bronze")
if st.session_state.score >= 100:
    badges.append("Silver")
if st.session_state.score >= 150:
    badges.append("Gold")

st.sidebar.write("Badges:", badges)

# -------------------------
# MAIN GAME
# -------------------------
st.title("⚡ AI Electrolysis WAEC Learning Game")

q = st.session_state.question
st.subheader("Level " + str(st.session_state.level))
st.write(q["question"])

choice = st.radio("Choose answer",
                  [q["option1"], q["option2"], q["option3"], q["option4"]])

col1, col2 = st.columns(2)

# SUBMIT BUTTON
with col1:
    if st.button("Submit"):
        if choice == q["answer"]:
            st.success("Correct")
            st.session_state.score += 10
            st.session_state.correct += 1

            if st.session_state.score >= (st.session_state.level * 40):
                st.session_state.level = min(st.session_state.level + 1, 3)

            st.session_state.question = get_question(st.session_state.level)
        else:
            st.error("Wrong")
            st.session_state.mistakes += 1
            st.info("Hint: " + q["hint"])

# NEXT BUTTON
with col2:
    if st.button("Next"):
        st.session_state.question = get_question(st.session_state.level)

# -------------------------
# PROGRESS BAR
# -------------------------
st.progress(min(st.session_state.score / 150, 1.0))

# -------------------------
# ANALYTICS
# -------------------------
attempts = st.session_state.correct + st.session_state.mistakes
accuracy = 0
if attempts > 0:
    accuracy = (st.session_state.correct / attempts) * 100

st.subheader("AI Performance")
st.metric("Accuracy", round(accuracy, 1))

# -------------------------
# AI RECOMMENDATION
# -------------------------
if accuracy < 50:
    st.error("AI Advice: Revise ion movement")
elif accuracy < 75:
    st.warning("AI Advice: Practice discharge")
else:
    st.success("AI Advice: Ready for exam")

# -------------------------
# LEARNING PANEL
# -------------------------
with st.expander("Review concept"):
    st.write("Topic:", q["topic"])
    st.write(q["hint"])

# -------------------------
# SAVE PROGRESS
# -------------------------
if st.button("Save Progress"):
    cursor.execute("""
        INSERT INTO students
        VALUES(?,?,?,?)
    """, (name, st.session_state.score, accuracy, st.session_state.level))
    conn.commit()
    st.success("Saved")

# -------------------------
# TEACHER DASHBOARD
# -------------------------
if st.checkbox("Teacher dashboard"):
    data = cursor.execute("SELECT * FROM students").fetchall()
    st.write(data)

# -------------------------
# EXAM MODE
# -------------------------
st.subheader("Exam Mode")
if st.button("Start WAEC Practice Test"):
    exam = df.sample(20)
    exam_score = 0
    for i, row in exam.iterrows():
        ans = st.radio(row["question"],
                       [row["option1"], row["option2"], row["option3"], row["option4"]],
                       key=i)
        if ans == row["answer"]:
            exam_score += 1
    if st.button("Submit Exam"):
        st.write("Score:", exam_score, "/20")

# -------------------------
# RESET GAME
# -------------------------
if st.button("Restart"):
    st.session_state.score = 0
    st.session_state.level = 1
    st.session_state.mistakes = 0
    st.session_state.correct = 0
    st.session_state.question = get_question(1)
    st.experimental_rerun()
col1,col2=st.columns(2)

with col1:

    if st.button("Submit"):

        if choice==q["answer"]:

            st.success("Correct")

            st.session_state.score+=10

            st.session_state.correct+=1

            if st.session_state.score>=(
            st.session_state.level*40):

                st.session_state.level=min(
                st.session_state.level+1,3)

            st.session_state.question= get_question(st.session_state.level)

        else:

            st.error("Wrong")

            st.session_state.mistakes+=1

            st.info("Hint: "+q["hint"])

with col2:

    if st.button("Next"):

        st.session_state.question= get_question(st.session_state.level)

# PROGRESS BAR

st.progress(min(st.session_state.score/150,1.0))

# ANALYTICS

attempts=st.session_state.correct+ st.session_state.mistakes

accuracy=0

if attempts>0:

    accuracy=(st.session_state.correct/
    attempts)*100

st.subheader("AI Performance")

st.metric("Accuracy",
round(accuracy,1))

# AI RECOMMENDATION

if accuracy<50:

    st.error("AI Advice: Revise ion movement")

elif accuracy<75:

    st.warning(
    "AI Advice: Practice discharge")

else:

    st.success(
    "AI Advice: Ready for exam")

# LEARNING PANEL

with st.expander("Review concept"):

    st.write("Topic:",q["topic"])

    st.write(q["hint"])

# SAVE

if st.button("Save Progress"):

    cursor.execute("""

    INSERT INTO students
    VALUES(?,?,?,?)

    """,(name,
    st.session_state.score,
    accuracy,
    st.session_state.level))

    conn.commit()

    st.success("Saved")

# TEACHER VIEW

if st.checkbox("Teacher dashboard"):

    data=cursor.execute(
    "SELECT * FROM students").fetchall()

    st.write(data)

# EXAM MODE

st.subheader("Exam Mode")

if st.button("Start WAEC Practice Test"):

    exam=df.sample(20)

    score=0

    for i,row in exam.iterrows():

        ans=st.radio(row["question"],

        [row["option1"],
        row["option2"],
        row["option3"],
        row["option4"]],

        key=i)

        if ans==row["answer"]:
            score+=1

    if st.button("Submit Exam"):

        st.write("Score:",score,"/20")

# RESET

if st.button("Restart"):

    st.session_state.score=0

    st.session_state.level=1

    st.session_state.mistakes=0

    st.session_state.correct=0

    st.session_state.question=
    get_question(1)

    st.rerun()
