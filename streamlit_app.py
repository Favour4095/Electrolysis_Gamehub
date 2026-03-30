import streamlit as st
import random

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

if "streak" not in st.session_state:
    st.session_state.streak=0

if "answered" not in st.session_state:
    st.session_state.answered=False

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

"electrolyte":"Mixed",

"ions":[

("Cu²⁺","Cathode"),
("Cl⁻","Anode")

]

}

}

lab=labs[st.session_state.lab]

# PLAYER PANEL

st.sidebar.title("Player")

st.sidebar.metric("Energy ⚡",
st.session_state.xp)

st.sidebar.metric("Lives ❤️",
st.session_state.lives)

st.sidebar.metric("Stars ⭐",
st.session_state.stars)

st.sidebar.metric("Streak 🔥",
st.session_state.streak)

# LAB PROGRESS

st.subheader("Lab Path")

cols=st.columns(5)

for i in range(1,6):

    if i<st.session_state.lab:

        cols[i-1].success("Lab "+str(i))

    elif i==st.session_state.lab:

        cols[i-1].info("Current")

    else:

        cols[i-1].write("🔒")

# LAB CARD

st.subheader(
"Lab "+str(st.session_state.lab)+
": "+lab["name"])

st.info(
"Electrolyte: "+
lab["electrolyte"])

# MATCHING GAME

st.write("Match ions to electrodes")

col1,col2,col3=st.columns(3)

with col1:

    ion1=st.selectbox(

    "Ion 1",

    [lab["ions"][0][0],
    lab["ions"][1][0]])

    ion2=st.selectbox(

    "Ion 2",

    [lab["ions"][0][0],
    lab["ions"][1][0]],

    key="ion2")

with col2:

    cathode=st.selectbox(

    "Cathode",

    [ion1,ion2])

with col3:

    anode=st.selectbox(

    "Anode",

    [ion1,ion2])

# SUBMIT

col1,col2=st.columns(2)

with col1:

    if st.button("Run Experiment"):

        correct=0

        for ion in lab["ions"]:

            if ion[0]==cathode and ion[1]=="Cathode":

                correct+=1

            if ion[0]==anode and ion[1]=="Anode":

                correct+=1

        if correct==2:

            st.success("Perfect experiment!")

            st.balloons()

            st.session_state.xp+=25

            st.session_state.stars+=1

            st.session_state.streak+=1

        else:

            st.error("Experiment failed")

            st.session_state.lives-=1

            st.session_state.streak=0

with col2:

    if st.button("Next Lab"):

        if st.session_state.lab<5:

            st.session_state.lab+=1

        st.rerun()

# PROGRESS

st.subheader("Mastery")

st.progress(

min(
st.session_state.xp/200,
1.0))

# LEVEL FEEDBACK

if st.session_state.streak>=3:

    st.success("Streak Bonus!")

    st.session_state.xp+=10

# ACHIEVEMENTS

st.subheader("Achievements")

if st.session_state.stars>=2:

    st.write("⭐ Ion Handler")

if st.session_state.stars>=4:

    st.write("⚡ Lab Expert")

if st.session_state.stars>=5:

    st.write("🏆 WAEC Ready")

# GAME OVER

if st.session_state.lives==0:

    st.error("Lab Closed")

    if st.button("Restart"):

        st.session_state.xp=0

        st.session_state.lab=1

        st.session_state.lives=3

        st.session_state.stars=0

        st.session_state.streak=0

        st.rerun()

# CONCEPT PANEL

with st.expander("Lab Notes"):

    st.write(
"Positive ions go to cathode")

    st.write(
"Negative ions go to anode")
