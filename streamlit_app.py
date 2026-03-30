import streamlit as st
import random

st.set_page_config(layout="wide")

st.title("⚡ Electrolysis Lab Game")

# SESSION

if "energy" not in st.session_state:
    st.session_state.energy=0

if "level" not in st.session_state:
    st.session_state.level=1

if "lives" not in st.session_state:
    st.session_state.lives=3

if "stars" not in st.session_state:
    st.session_state.stars=0

if "streak" not in st.session_state:
    st.session_state.streak=0


# GAME DATA

game_data=[

{

"electrolyte":"NaCl",

"ions":[

("Na+","Cathode"),

("Cl-","Anode")

]

},

{

"electrolyte":"CuSO4",

"ions":[

("Cu2+","Cathode"),

("SO4-","Anode")

]

}

]

current=random.choice(game_data)

st.subheader("Level "+str(
st.session_state.level))

st.info("Electrolyte: "+
current["electrolyte"])


# UI

col1,col2,col3=st.columns(3)

with col1:

    st.subheader("Ions")

    ion1=st.selectbox(
    "Ion 1",

    [current["ions"][0][0],
    current["ions"][1][0]])

    ion2=st.selectbox(
    "Ion 2",

    [current["ions"][0][0],
    current["ions"][1][0]])

with col2:

    st.subheader("Cathode")

    cathode1=st.selectbox(
    "Drop ion",

    [ion1,ion2])

with col3:

    st.subheader("Anode")

    anode1=st.selectbox(
    "Drop ion",

    [ion1,ion2])

# SUBMIT

if st.button("Run Experiment"):

    correct=0

    if cathode1=="Na+" or cathode1=="Cu2+":
        correct+=1

    if anode1=="Cl-" or anode1=="SO4-":
        correct+=1

    if correct==2:

        st.success("Perfect experiment!")

        st.balloons()

        st.session_state.energy+=20

        st.session_state.stars+=1

        st.session_state.streak+=1

    else:

        st.error("Experiment failed")

        st.session_state.lives-=1

        st.session_state.streak=0

# PLAYER PANEL

st.sidebar.title("Player")

st.sidebar.metric("Energy ⚡",
st.session_state.energy)

st.sidebar.metric("Stars ⭐",
st.session_state.stars)

st.sidebar.metric("Lives ❤️",
st.session_state.lives)

st.sidebar.metric("Streak 🔥",
st.session_state.streak)

# PROGRESS

st.progress(
min(st.session_state.energy/200,1.0))

# LEVEL UP

if st.session_state.energy>=
(st.session_state.level*100):

    st.session_state.level+=1

    st.success("New lab unlocked!")

# GAME OVER

if st.session_state.lives==0:

    st.error("Lab closed")

    if st.button("Restart"):

        st.session_state.energy=0

        st.session_state.level=1

        st.session_state.lives=3

        st.session_state.stars=0

        st.rerun()
