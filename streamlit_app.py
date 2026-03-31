import streamlit as st
import random

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

if "lab_question" not in st.session_state:
    st.session_state.lab_question=0

if "answered" not in st.session_state:
    st.session_state.answered=False

# LAB DATA

labs={

1:{
"name":"Ion Movement",
"electrolyte":"NaCl",

"questions":[

{"ions":[("Na⁺","Cathode"),("Cl⁻","Anode")],
"hint":"Positive ions go to cathode"},

{"ions":[("H⁺","Cathode"),("Cl⁻","Anode")],
"hint":"Hydrogen forms at cathode"},

{"ions":[("K⁺","Cathode"),("Br⁻","Anode")],
"hint":"Metals move to cathode"},

{"ions":[("Ag⁺","Cathode"),("NO₃⁻","Anode")],
"hint":"Silver deposits"},

{"ions":[("Cu²⁺","Cathode"),("Cl⁻","Anode")],
"hint":"Copper is reduced"}

]

},

2:{
"name":"Copper Sulphate",
"electrolyte":"CuSO₄",

"questions":[

{"ions":[("Cu²⁺","Cathode"),("SO₄²⁻","Anode")],
"hint":"Copper plates out"},

{"ions":[("H⁺","Cathode"),("SO₄²⁻","Anode")],
"hint":"Hydrogen may form"},

{"ions":[("Cu²⁺","Cathode"),("OH⁻","Anode")],
"hint":"Oxygen may form"},

{"ions":[("Cu²⁺","Cathode"),("Cl⁻","Anode")],
"hint":"Copper still deposits"},

{"ions":[("H⁺","Cathode"),("OH⁻","Anode")],
"hint":"Water electrolysis"}

]

},

3:{
"name":"Dilute Acid",
"electrolyte":"H₂SO₄",

"questions":[

{"ions":[("H⁺","Cathode"),("SO₄²⁻","Anode")],
"hint":"Hydrogen forms"},

{"ions":[("H⁺","Cathode"),("OH⁻","Anode")],
"hint":"Water splits"},

{"ions":[("Na⁺","Cathode"),("SO₄²⁻","Anode")],
"hint":"Na stays in solution"},

{"ions":[("H⁺","Cathode"),("Cl⁻","Anode")],
"hint":"Acid behaviour"},

{"ions":[("H⁺","Cathode"),("NO₃⁻","Anode")],
"hint":"Hydrogen forms"}

]

},

4:{
"name":"Brine",
"electrolyte":"NaCl(aq)",

"questions":[

{"ions":[("H⁺","Cathode"),("Cl⁻","Anode")],
"hint":"Chlorine forms"},

{"ions":[("Na⁺","Cathode"),("Cl⁻","Anode")],
"hint":"Na does not discharge"},

{"ions":[("H⁺","Cathode"),("OH⁻","Anode")],
"hint":"Oxygen possible"},

{"ions":[("H⁺","Cathode"),("Cl⁻","Anode")],
"hint":"Hydrogen gas forms"},

{"ions":[("Na⁺","Cathode"),("OH⁻","Anode")],
"hint":"Na remains dissolved"}

]

},

5:{
"name":"WAEC Challenge",
"electrolyte":"Mixed Cell",

"questions":[

{"ions":[("Cu²⁺","Cathode"),("Cl⁻","Anode")],
"hint":"Less reactive metal deposits"},

{"ions":[("Ag⁺","Cathode"),("NO₃⁻","Anode")],
"hint":"Silver deposits"},

{"ions":[("H⁺","Cathode"),("SO₄²⁻","Anode")],
"hint":"Hydrogen gas forms"},

{"ions":[("Cu²⁺","Cathode"),("OH⁻","Anode")],
"hint":"Copper reduces"},

{"ions":[("H⁺","Cathode"),("Cl⁻","Anode")],
"hint":"Chlorine forms"}

]

}

}

lab=labs[st.session_state.lab]

question=lab["questions"][st.session_state.lab_question]

ions=[
question["ions"][0][0],
question["ions"][1][0]
]

# SIDEBAR

st.sidebar.title("Player")

st.sidebar.metric("XP ⚡",st.session_state.xp)

st.sidebar.metric("Lives ❤️",st.session_state.lives)

st.sidebar.metric("Stars ⭐",st.session_state.stars)

st.sidebar.metric("Streak 🔥",st.session_state.streak)

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
"Lab "+str(st.session_state.lab)+
": "+lab["name"])

st.write(
"Question",
st.session_state.lab_question+1,
"/5")

st.info(
"Electrolyte: "+
lab["electrolyte"])

# LAB UI

col1,col2,col3=st.columns(3)

with col1:

    st.error("ANODE (+)")

    anode=st.selectbox(
    "Ion at anode",
    ions)

with col2:

    st.info("Electrolyte")

    st.write("Available ions")

    st.write(ions[0])

    st.write(ions[1])

with col3:

    st.success("CATHODE (-)")

    cathode=st.selectbox(
    "Ion at cathode",
    ions)

# HINT

if st.button("💡 Hint"):

    st.info(question["hint"])

# RUN EXPERIMENT

if st.button("Run Experiment"):

    if st.session_state.answered==False:

        correct=0

        for ion in question["ions"]:

            if ion[0]==anode and ion[1]=="Anode":
                correct+=1

            if ion[0]==cathode and ion[1]=="Cathode":
                correct+=1

        if correct==2:

            st.success("Correct!")

            st.balloons()

            st.session_state.xp+=20

            st.session_state.stars+=1

            st.session_state.streak+=1

            st.session_state.answered=True

        else:

            st.error("Wrong")

            st.session_state.lives-=1

            st.session_state.streak=0

# NEXT QUESTION

if st.button("Next Question"):

    if st.session_state.answered:

        st.session_state.lab_question+=1

        st.session_state.answered=False

        if st.session_state.lab_question>=5:

            st.success("Lab Completed!")

            st.session_state.xp+=50

            st.session_state.lab+=1

            st.session_state.lab_question=0

        st.rerun()

    else:

        st.warning("Solve question first")

# STREAK BONUS

if st.session_state.streak>=3:

    st.success("🔥 Streak Bonus +15 XP")

    st.session_state.xp+=15

    st.session_state.streak=0

# XP BAR

st.subheader("Mastery Level")

st.progress(min(st.session_state.xp/500,1.0))

# GAME OVER

if st.session_state.lives<=0:

    st.error("Game Over")

    if st.button("Restart"):

        st.session_state.xp=0

        st.session_state.lab=1

        st.session_state.lives=3

        st.session_state.stars=0

        st.session_state.streak=0

        st.session_state.lab_question=0

        st.session_state.answered=False

        st.rerun()

# GAME COMPLETE

if st.session_state.lab>5:

    st.success("🏆 Electrolysis Master!")

    st.balloons()

# LEARNING NOTES

with st.expander("Lab Notes"):

    st.write("Oxidation occurs at anode")

    st.write("Reduction occurs at cathode")

    st.write("Cations gain electrons")

    st.write("Anions lose electrons")
