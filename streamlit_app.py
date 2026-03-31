import streamlit as st
import pandas as pd
import sqlite3
import random

st.set_page_config(page_title="Electrolysis Adventure",layout="wide")

# LOAD CSV
df = pd.read_csv("Questions.csv")

# CLEAN COLUMN NAMES
df.columns=df.columns.str.strip()

# DATABASE
conn=sqlite3.connect("students.db",check_same_thread=False)

cursor=conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS students(

name TEXT,
xp INTEGER,
score INTEGER

)

""")

# SESSION STATE

if "questions" not in st.session_state:

    st.session_state.questions=df.sample(frac=1).reset_index(drop=True)

if "q_index" not in st.session_state:

    st.session_state.q_index=0

if "xp" not in st.session_state:

    st.session_state.xp=0

if "score" not in st.session_state:

    st.session_state.score=0

if "lives" not in st.session_state:

    st.session_state.lives=3

if "game_over" not in st.session_state:

    st.session_state.game_over=False


# RESET FUNCTION

def reset_game():

    st.session_state.questions=df.sample(frac=1).reset_index(drop=True)

    st.session_state.q_index=0

    st.session_state.xp=0

    st.session_state.score=0

    st.session_state.lives=3

    st.session_state.game_over=False


# HEADER

st.title("Electrolysis Adventure Game")

st.progress(st.session_state.xp/500)

c1,c2,c3=st.columns(3)

c1.metric("XP",st.session_state.xp)

c2.metric("Lives",st.session_state.lives)

c3.metric("Score",st.session_state.score)


# GAME OVER

if st.session_state.lives<=0:

    st.error("Game Over")

    st.session_state.game_over=True

    if st.button("Restart"):

        reset_game()

        st.rerun()

    st.stop()


# GET QUESTION

q=st.session_state.questions.iloc[st.session_state.q_index]

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

if st.button("Submit Answer"):

    letters=['A','B','C','D']

    selected_letter=letters[options.index(answer)]

    if selected_letter==q['answer']:

        st.success("Correct")

        st.balloons()

        st.session_state.score+=10

        st.session_state.xp+=20

    else:

        st.error("Wrong answer")

        st.session_state.lives-=1

        st.info("Hint: "+str(q['hint']))


# NEXT QUESTION

if st.button("Next Question"):

    st.session_state.q_index+=1

    if st.session_state.q_index>=len(st.session_state.questions):

        st.session_state.q_index=0

    st.rerun()


# RESET

if st.button("Reset Game"):

    reset_game()

    st.rerun()


st.divider()

# LAB SECTION (VERSION 7 STYLE)

st.header("Virtual Electrolysis Lab")

st.write("Select ions that move to Cathode")

ions=['H+','Na+','Cu2+','Cl-','OH-','SO4-']

selected=st.multiselect(

"Select ions",

ions

)

if st.button("Submit Lab"):

    correct=['H+','Na+','Cu2+']

    if any(i in selected for i in correct):

        st.success("Good work")

        st.balloons()

        st.session_state.xp+=30

    else:

        st.error("Check charges again")


st.divider()

# SAVE PLAYER

st.subheader("Save Progress")

name=st.text_input("Player name")

if st.button("Save"):

    if name!="":

        cursor.execute(

        "INSERT INTO students VALUES(?,?,?)",

        (name,st.session_state.xp,st.session_state.score)

        )

        conn.commit()

        st.success("Progress saved")
