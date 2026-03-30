import streamlit as st
import random
import time

st.set_page_config(layout="wide")

st.title("⚡ Electrolysis Quest – Virtual Lab")

# PLAYER STATE

if "xp" not in st.session_state:
    st.session_state.xp=0

if "lab" not in st.session_state:
    st.session_state.lab=1

if "lives" not in st.session_state:
    st.session_state.lives=3

if "stars" not in st.session_state:
    st.session_state.stars=0

if "streak" not in st.session_state:
    st.session_state.streak=0

if "time_left" not in st.session_state:
    st.session_state.time_left=20

# LAB DATA

labs={

1:{

"name":"Ion Movement",

"electrolyte":"NaCl",

"ions":[

("Na⁺","Cathode"),
("Cl⁻","Anode")

]

},

2:{

"name":"Copper Sulphate",

"electrolyte":"CuSO₄",

"ions":[

("Cu²⁺","Cathode"),
("SO₄²⁻","Anode")

]

},

3:{

"name":"Dilute Acid",

"electrolyte":"H₂SO₄",

"ions":[

("H⁺","Cathode"),
("SO₄²⁻","Anode")

]

},

4:{

"name":"Brine",

"electrolyte":"NaCl(aq)",

"ions":[

("H⁺","Cathode"),
("Cl⁻","Anode")

]

},

5:{

"name":"WAEC Challenge",

"electrolyte":"Mixed Cell",

"ions":[

("Cu²⁺","Cathode"),
("Cl⁻","Anode")

]

}

}

lab=labs[st.session_state.lab]

# SIDEBAR PLAYER PANEL

st.sidebar.title("Player")

st.sidebar.metric("Energy ⚡",
st.session_state.xp)

st.sidebar.metric("Lives ❤️",
st.session_state.lives)

st.sidebar.metric("Stars ⭐",
st.session_state.stars)

st.sidebar.metric("Streak 🔥",
st.session_state.streak)

# LAB MAP

st.subheader("Lab Progress")

cols=st.columns(5)

for i in range(1,6):

    if i<st.session_state.lab:

        cols[i-1].success("✔")

    elif i==st.session_state.lab:

        cols[i-1].info("Current")

    else:

        cols[i-1].write("🔒")

# LAB INFO

st.subheader(
"Lab "+str(st.session_state.lab)+ ": "+lab["name"])

st.info(
"Electrolyte: "+ lab["electrolyte"])

# TIMER

st.write("⏱ Time Challenge")

st.progress(
st.session_state.time_left/20)

# VISUAL LAB LAYOUT

st.write("### Virtual Electrolysis Cell")

col1,col2,col3=st.columns(3)

with col1:

    st.error("ANODE (+)")

    anode=st.selectbox(

    "Ion at anode",

    [lab["ions"][0][0],
    lab["ions"][1][0]])

with col2:

    st.info("Electrolyte")

    st.write(
    lab["ions"][0][0],
    lab["ions"][1][0])

with col3:

    st.success("CATHODE (-)")

    cathode=st.selectbox(

    "Ion at cathode",

    [lab["ions"][0][0],
    lab["ions"][1][0]])

# EXPERIMENT BUTTONS

col1,col2=st.columns(2)

with col1:

    if st.button("Run Experiment"):

        correct=0

        for ion in lab["ions"]:

            if ion[0]==anode and ion[1]=="Anode":

                correct+=1

            if ion[0]==cathode and ion[1]=="Cathode":

                correct+=1

        if correct==2:

            st.success("Experiment successful!")

            st.balloons()

            st.session_state.xp+=30

            st.session_state.stars+=1

            st.session_state.streak+=1

        else:

            st.error("Wrong placement")

            st.session_state.lives-=1

            st.session_state.streak=0

with col2:

    if st.button("Next Lab"):

        if st.session_state.lab<5:

            st.session_state.lab+=1

            st.session_state.time_left=20

        st.rerun()

# STREAK BONUS

if st.session_state.streak>=3:

    st.success("🔥 Streak bonus +10 XP")

    st.session_state.xp+=10

# PROGRESS BAR

st.subheader("Mastery Level")

st.progress(

min(
st.session_state.xp/250,
1.0))

# ACHIEVEMENTS

st.subheader("Achievements")

if st.session_state.stars>=2:

    st.write("⭐ Ion Handler")

if st.session_state.stars>=4:

    st.write("⚡ Lab Expert")

if st.session_state.stars>=5:

    st.write("🏆 Electrolysis Master")

# GAME OVER

if st.session_state.lives==0:

    st.error("Game Over")

    if st.button("Restart"):

        st.session_state.xp=0

        st.session_state.lab=1

        st.session_state.lives=3

        st.session_state.stars=0

        st.session_state.streak=0

        st.rerun()

# LEARNING PANEL

with st.expander("Lab Notes"):

    st.write(
"Oxidation occurs at the anode")

    st.write(
"Reduction occurs at the cathode")

    st.write(
"Positive ions gain electrons")

    st.write(
"Negative ions lose electrons")
