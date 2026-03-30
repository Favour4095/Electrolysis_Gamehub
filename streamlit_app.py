import streamlit as st
import random
import pandas as pd

st.set_page_config(layout="wide")

st.title("⚡ Electrolysis Quest")

# PLAYER STATE

if "xp" not in st.session_state:
    st.session_state.xp=0

if "lab" not in st.session_state:
    st.session_state.lab=1

if "lives" not in st.session_state:
    st.session_state.lives=3

if "stars" not in st.session_state:
    st.session_state.stars=0

if "exam_mode" not in st.session_state:
    st.session_state.exam_mode=False

if "exam_score" not in st.session_state:
    st.session_state.exam_score=0

if "exam_started" not in st.session_state:
    st.session_state.exam_started=False

if "weak_topic" not in st.session_state:
    st.session_state.weak_topic="None"

# LAB DATA

labs={

1:("Na⁺ goes to?","Cathode","Ion movement"),

2:("Product at cathode CuSO4?",
"Copper","Products"),

3:("Which discharges first?",
"Cu²⁺","Discharge"),

4:("Gas at anode NaCl?",
"Chlorine","Observation"),

5:("Cathode product dilute acid?",
"Hydrogen","WAEC")

}

# EXAM QUESTIONS

exam_questions=[

("Na⁺ goes to?",
["Anode","Cathode"],
"Cathode",
"Ion movement"),

("Product at cathode CuSO4?",
["Copper","Oxygen"],
"Copper",
"Products"),

("Gas at anode?",
["Chlorine","Hydrogen"],
"Chlorine",
"Observation"),

("Discharge first?",
["Cu²⁺","H⁺"],
"Cu²⁺",
"Discharge")

]

# PLAYER PANEL

st.sidebar.title("Player")

st.sidebar.metric("Energy ⚡",
st.session_state.xp)

st.sidebar.metric("Lives ❤️",
st.session_state.lives)

st.sidebar.metric("Stars ⭐",
st.session_state.stars)

# MENU

mode=st.radio(

"Select Mode",

["Play Labs",
"WAEC Exam",
"Performance"])

# LAB MODE

if mode=="Play Labs":

    question=labs[st.session_state.lab]

    st.subheader(
    "Lab "+str(
    st.session_state.lab))

    st.info(question[0])

    ans=st.radio(

    "Answer",

    ["Anode",
    "Cathode",
    "Copper",
    "Hydrogen",
    "Chlorine",
    "Cu²⁺"])

    if st.button("Submit"):

        if ans==question[1]:

            st.success("Correct")

            st.balloons()

            st.session_state.xp+=20

            st.session_state.stars+=1

        else:

            st.error("Wrong")

            st.session_state.lives-=1

            st.session_state.weak_topic= question[2]

    if st.button("Next"):

        if st.session_state.lab<5:

            st.session_state.lab+=1

        st.rerun()

# EXAM MODE

if mode=="WAEC Exam":

    st.subheader("WAEC Practice Test")

    score=0

    answers=[]

    for i,q in enumerate(exam_questions):

        choice=st.radio(

        q[0],

        q[1],

        key=i)

        answers.append((choice,q))

    if st.button("Submit Exam"):

        weak=[]

        for a in answers:

            if a[0]==a[1][2]:

                score+=1

            else:

                weak.append(a[1][3])

        st.session_state.exam_score=score

        if len(weak)>0:

            st.session_state.weak_topic= random.choice(weak)

        st.success(
        "Score: "+str(score)+ "/"+str(len(exam_questions)))

# PERFORMANCE MODE

if mode=="Performance":

    st.subheader("Performance Report")

    st.metric("Exam Score",
    st.session_state.exam_score)

    st.metric("XP",
    st.session_state.xp)

    st.metric("Stars",
    st.session_state.stars)

    st.metric("Weak Topic",
    st.session_state.weak_topic)

    if st.session_state.exam_score<2:

        st.error(
        "Revise basics")

    elif st.session_state.exam_score<3:

        st.warning(
        "Practice more")

    else:

        st.success(
        "WAEC Ready")

# GAME OVER

if st.session_state.lives==0:

    st.error("Game Over")

    if st.button("Restart"):

        st.session_state.xp=0

        st.session_state.lab=1

        st.session_state.lives=3

        st.session_state.stars=0

        st.rerun()
