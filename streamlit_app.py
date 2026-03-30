import streamlit as st
import random

st.set_page_config(layout="wide")

st.title("⚡ Electrolysis Quest")

# SESSION STATE

if "xp" not in st.session_state:
    st.session_state.xp=0

if "level" not in st.session_state:
    st.session_state.level=1

if "lives" not in st.session_state:
    st.session_state.lives=3

if "stars" not in st.session_state:
    st.session_state.stars=0

if "streak" not in st.session_state:
    st.session_state.streak=0

if "answered" not in st.session_state:
    st.session_state.answered=False

# GAME QUESTIONS

labs=[

{

"electrolyte":"NaCl",

"question":"Where will Na+ go?",

"options":[

"Anode",
"Cathode"

],

"answer":"Cathode",

"hint":"Positive ions go to cathode"

},

{

"electrolyte":"CuSO4",

"question":"Where will Cu2+ go?",

"options":[

"Anode",
"Cathode"

],

"answer":"Cathode",

"hint":"Metals deposit at cathode"

}

]

lab=random.choice(labs)

# PLAYER PANEL

st.sidebar.title("Player")

st.sidebar.metric("Energy ⚡",
st.session_state.xp)

st.sidebar.metric("Stars ⭐",
st.session_state.stars)

st.sidebar.metric("Lives ❤️",
st.session_state.lives)

st.sidebar.metric("Streak 🔥",
st.session_state.streak)

st.sidebar.metric("Level",
st.session_state.level)

# GAME CARD

st.subheader(
"Experiment "+str(
st.session_state.level))

st.info(
"Electrolyte: "+ lab["electrolyte"])

st.write(lab["question"])

choice=st.radio(

"Select",

lab["options"])

# BUTTONS

col1,col2=st.columns(2)

with col1:

    if st.button("Submit"):

        st.session_state.answered=True

        if choice==lab["answer"]:

            st.success("Correct!")

            st.balloons()

            st.session_state.xp+=15

            st.session_state.stars+=1

            st.session_state.streak+=1

        else:

            st.error("Wrong")

            st.write(
            "Hint:",
            lab["hint"])

            st.session_state.lives-=1

            st.session_state.streak=0

with col2:

    if st.button("Next"):

        st.session_state.answered=False

        st.rerun()

# PROGRESS BAR

st.subheader(
"Progress to next lab")

st.progress(

min(
st.session_state.xp/200,
1.0))

# LEVEL UP

if st.session_state.xp>= (st.session_state.level*80):

    st.session_state.level+=1

    st.success(
"New experiment unlocked!")

# GAME OVER

if st.session_state.lives==0:

    st.error(
"Game Over")

    if st.button("Restart"):

        st.session_state.xp=0

        st.session_state.level=1

        st.session_state.lives=3

        st.session_state.stars=0

        st.session_state.streak=0

        st.rerun()

# ACHIEVEMENTS

st.subheader("Achievements")

if st.session_state.stars>=5:

    st.write("⭐ Ion Master")

if st.session_state.stars>=10:

    st.write("⚡ Electrolysis Pro")

if st.session_state.stars>=20:

    st.write("🏆 WAEC Ready")

# LEARNING PANEL

with st.expander(
"Learn concept"):

    st.write(
"Positive ions move to cathode")

    st.write(
"Negative ions move to anode")
