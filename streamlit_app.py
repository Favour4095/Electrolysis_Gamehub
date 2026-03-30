import streamlit as st
import pandas as pd
import random
import sqlite3

st.set_page_config(page_title="Electrolysis Game",
layout="wide")

# LOAD QUESTIONS
df=pd.read_csv("Questions.csv")

# DATABASE
conn=sqlite3.connect("students.db",
check_same_thread=False)

cursor=conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS students(

name TEXT,
score INTEGER,
accuracy REAL,
level INTEGER

)

""")

conn.commit()

# SESSION STATE

if "score" not in st.session_state:
    st.session_state.score=0

if "level" not in st.session_state:
    st.session_state.level=1

if "mistakes" not in st.session_state:
    st.session_state.mistakes=0

if "correct" not in st.session_state:
    st.session_state.correct=0

if "lives" not in st.session_state:
    st.session_state.lives=3

if "streak" not in st.session_state:
    st.session_state.streak=0

if "answered" not in st.session_state:
    st.session_state.answered=False

if "feedback" not in st.session_state:
    st.session_state.feedback=""

if "name" not in st.session_state:
    st.session_state.name=""

def get_question(level):

    subset=df[df["level"]==level]

    return subset.sample(1).iloc[0]

if "question" not in st.session_state:

    st.session_state.question=get_question(1)

# SIDEBAR

st.sidebar.title("🎮 Player Profile")

name=st.sidebar.text_input("Name")

st.session_state.name=name

st.sidebar.metric("XP",st.session_state.score)

st.sidebar.metric("Level",
st.session_state.level)

st.sidebar.metric("Streak 🔥",
st.session_state.streak)

st.sidebar.metric("Lives ❤️",
st.session_state.lives)

# BADGES

badges=[]

if st.session_state.score>=50:
    badges.append("🥉 Bronze")

if st.session_state.score>=100:
    badges.append("🥈 Silver")

if st.session_state.score>=150:
    badges.append("🥇 Gold")

st.sidebar.write("Achievements")

st.sidebar.write(badges)

# MAIN GAME

st.title("⚡ Electrolysis Master Game")

q=st.session_state.question

st.subheader("Level "+
str(st.session_state.level))

st.info(q["question"])

choice=st.radio("Select answer",

[q["option1"],
q["option2"],
q["option3"],
q["option4"]],

key="choice")

col1,col2=st.columns(2)

with col1:

    if st.button("Submit") and not st.session_state.answered:

        st.session_state.answered=True

        if choice==q["answer"]:

            st.session_state.feedback="correct"

            st.session_state.score+=10

            st.session_state.correct+=1

            st.session_state.streak+=1

            # streak bonus

            if st.session_state.streak>=3:

                st.session_state.score+=5

                st.balloons()

            if st.session_state.score>=(
            st.session_state.level*40):

                st.session_state.level=min(
                st.session_state.level+1,3)

        else:

            st.session_state.feedback="wrong"

            st.session_state.mistakes+=1

            st.session_state.lives-=1

            st.session_state.streak=0

with col2:

    if st.button("Next"):

        st.session_state.question= get_question(
        st.session_state.level)

        st.session_state.answered=False

        st.session_state.feedback=""

        st.rerun()

# FEEDBACK PANEL

if st.session_state.answered:

    if st.session_state.feedback=="correct":

        st.success("✅ Correct!")

    else:

        st.error("❌ Wrong")

        st.write("Hint:",
        q["hint"])

# GAME OVER

if st.session_state.lives==0:

    st.error("Game Over")

    st.button("Restart")

# PROGRESS

st.subheader("Progress to next level")

progress=min(
st.session_state.score/150,1.0)

st.progress(progress)

# ANALYTICS

attempts=(st.session_state.correct+ st.session_state.mistakes)

accuracy=0

if attempts>0:

    accuracy=(st.session_state.correct/
    attempts)*100

st.subheader("Performance")

col1,col2=st.columns(2)

col1.metric("Accuracy",
round(accuracy,1))

col2.metric("Questions answered",
attempts)

# AI ADVICE

if accuracy<50:

    st.error(
"Revise electrolysis basics")

elif accuracy<75:

    st.warning(
"Practice more questions")

else:

    st.success(
"Ready for WAEC")

# LEARNING PANEL

with st.expander("Review concept"):

    st.write("Topic:",
    q["topic"])

    st.write(q["hint"])

# SAVE

if st.button("Save Progress"):

    cursor.execute("""

INSERT INTO students
VALUES(?,?,?,?)

""",

(st.session_state.name,

st.session_state.score,

accuracy,

st.session_state.level))

    conn.commit()

    st.success("Progress saved")

# RESET

if st.button("Restart Game"):

    st.session_state.score=0

    st.session_state.level=1

    st.session_state.mistakes=0

    st.session_state.correct=0

    st.session_state.lives=3

    st.session_state.streak=0

    st.session_state.question= get_question(1)

    st.session_state.answered=False

    st.rerun()
