import streamlit as st
import pandas as pd
import random
import sqlite3

st.set_page_config(page_title="Electrolysis Game", layout="wide")

# LOAD QUESTIONS
df = pd.read_csv("electrolysis_questions.csv")

# DATABASE
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
name TEXT,
xp INTEGER,
level INTEGER
)
""")

# SESSION STATE
if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "lives" not in st.session_state:
    st.session_state.lives = 3

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "questions" not in st.session_state:
    st.session_state.questions = df.sample(len(df)).reset_index()

# RESET FUNCTION
def reset_game():

    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.lives = 3
    st.session_state.xp = 0
    st.session_state.game_over = False
    st.session_state.questions = df.sample(len(df)).reset_index()


st.title("Electrolysis Adventure Game")

st.progress(st.session_state.xp/500)

col1,col2,col3 = st.columns(3)

col1.metric("XP",st.session_state.xp)
col2.metric("Lives",st.session_state.lives)
col3.metric("Score",st.session_state.score)

# GAME OVER
if st.session_state.lives == 0:

    st.error("Game Over")

    st.session_state.game_over = True

    if st.button("Restart"):
        reset_game()

    st.stop()


# GET CURRENT QUESTION
q = st.session_state.questions.iloc[st.session_state.question_index]

st.subheader(q['question'])

options = [
q['optionA'],
q['optionB'],
q['optionC'],
q['optionD']
]

answer = st.radio(
"Select answer",
options,
key=st.session_state.question_index
)

# SUBMIT BUTTON
if st.button("Submit"):

    correct = q['answer']

    selected_letter = options.index(answer)

    letters=['A','B','C','D']

    if letters[selected_letter] == correct:

        st.success("Correct!")

        st.balloons()

        st.session_state.score +=10

        st.session_state.xp +=20

    else:

        st.error("Wrong")

        st.session_state.lives -=1


# NEXT BUTTON
if st.button("Next Question"):

    if not st.session_state.game_over:

        st.session_state.question_index +=1

        if st.session_state.question_index >= len(st.session_state.questions):

            st.session_state.question_index=0

        st.rerun()


# RESET
if st.button("Reset Game"):

    reset_game()

    st.rerun()


st.divider()

# LAB SECTION (UNCHANGED STYLE)

st.header("Virtual Electrolysis Lab")

st.write("Drag ions to correct electrodes")

colA,colB = st.columns(2)

with colA:

    st.subheader("Anode (+)")

    st.info("Place negative ions")

with colB:

    st.subheader("Cathode (-)")

    st.info("Place positive ions")

ions=['H+','Cu2+','OH-','Cl-']

selected = st.multiselect("Select ions for Cathode",ions)

if st.button("Submit Lab"):

    if 'H+' in selected or 'Cu2+' in selected:

        st.success("Good job")

        st.session_state.xp+=30

    else:

        st.error("Check ion charges")

st.divider()

# PLAYER SAVE

name = st.text_input("Player Name")

if st.button("Save Progress"):

    cursor.execute(
    "INSERT INTO students VALUES(?,?,?)",
    (name,st.session_state.xp,1)
    )

    conn.commit()

    st.success("Saved")
