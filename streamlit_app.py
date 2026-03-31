import streamlit as st
import pandas as pd
import random
import sqlite3

st.set_page_config(page_title="Electrolysis Adventure", layout="wide")

# LOAD QUESTIONS
df = pd.read_csv("electrolysis_questions.csv")

# CLEAN COLUMNS (prevents optionA errors)
df.columns = df.columns.str.strip().str.lower()

# DATABASE
conn = sqlite3.connect("students.db",check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
name TEXT,
xp INTEGER,
score INTEGER
)
""")

# SESSION STATES

if "questions" not in st.session_state:

    st.session_state.questions = df.sample(frac=1).reset_index(drop=True)

if "q_index" not in st.session_state:

    st.session_state.q_index = 0

if "score" not in st.session_state:

    st.session_state.score = 0

if "xp" not in st.session_state:

    st.session_state.xp = 0

if "lives" not in st.session_state:

    st.session_state.lives = 3

if "game_over" not in st.session_state:

    st.session_state.game_over=False


# RESET FUNCTION

def reset_game():

    st.session_state.questions = df.sample(frac=1).reset_index(drop=True)

    st.session_state.q_index=0

    st.session_state.score=0

    st.session_state.xp=0

    st.session_state.lives=3

    st.session_state.game_over=False


# HEADER

st.title("Electrolysis Adventure Game")

st.progress(st.session_state.xp/500)

c1,c2,c3=st.columns(3)

c1.metric("XP",st.session_state.xp)

c2.metric("Lives",st.session_state.lives)

c3.metric("Score",st.session_state.score)


# GAME OVER CHECK

if st.session_state.lives<=0:

    st.error("Game Over")

    st.session_state.game_over=True

    if st.button("Restart Game"):

        reset_game()

        st.rerun()

    st.stop()


# CURRENT QUESTION

q = st.session_state.questions.iloc[st.session_state.q_index]

st.subheader(q['questions'])

options=[

q['optionA'],

q['optionB'],

q['optionC'],

q['optionD']

]


answer=st.radio(

"Choose answer",

options,

key="answer_select"

)



# SUBMIT
p
if st.button("Submit Answer"):

    if not st.session_state.game_over:

        letters=['A','B','C','D']

        selected_letter=letters[options.index(answer)]

        if selected_letter==q['answer']:

            st.success("Correct!")

            st.balloons()

            st.session_state.score+=10

            st.session_state.xp+=20

        else:

            st.error("Wrong answer")

            st.session_state.lives-=1


# NEXT QUESTION

if st.button("Next Question"):

    if not st.session_state.game_over:

        st.session_state.q_index+=1

        if st.session_state.q_index>=len(st.session_state.questions):

            st.session_state.q_index=0

        st.rerun()


# RESET BUTTON

if st.button("Reset Game"):

    reset_game()

    st.rerun()


st.divider()


# LAB SECTION (VERSION 7 STYLE)

st.header("Virtual Electrolysis Lab")
st.write("Place ions correctly to earn XP")

col1,col2=st.columns(2)

with col1:

    st.subheader("Anode (+)")

    st.info("Negative ions go here")

with col2:

    st.subheader("Cathode (-)")

    st.info("Positive ions go here")


ions=['H+','Cu2+','Na+','OH-','Cl-','SO4-']

selected=st.multiselect(

"Select ions that go to Cathode",

ions

)


if st.button("Submit Lab Work"):

    correct=['H+','Cu2+','Na+']

    if any(i in selected for i in correct):

        st.success("Good laboratory work")

        st.balloons()

        st.session_state.xp+=30

    else:

        st.error("Review ion charges")


st.divider()


# SAVE PLAYER

st.subheader("Save Progress")

name=st.text_input("Player Name")

if st.button("Save Progress"):

    if name!="":

        cursor.execute(

        "INSERT INTO students VALUES(?,?,?)",

        (name,st.session_state.xp,st.session_state.score)

        )

        conn.commit()

        st.success("Progress saved")


# FOOTER

st.caption("Educational Electrolysis Game - SS2 Chemistry")
