import streamlit as st
import pandas as pd
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

"question":
"Where will Na⁺ move?",

"options":
["Anode","Cathode"],

"answer":
"Cathode",

"hint":
"Positive ions move to cathode"

},

2:{

"name":"Electrode Products",

"question":
"What forms at cathode in CuSO₄?",

"options":
["Copper","Oxygen"],

"answer":
"Copper",

"hint":
"Metals deposit at cathode"

},

3:{

"name":"Discharge Rules",

"question":
"Which ion discharges first?",

"options":
["Cu²⁺","H⁺"],

"answer":
"Cu²⁺",

"hint":
"Less reactive metals discharge"

},

4:{

"name":"Observation",

"question":
"Gas at anode in NaCl?",

"options":
["Chlorine","Hydrogen"],

"answer":
"Chlorine",

"hint":
"Halides form gas"

},

5:{

"name":"WAEC Challenge",

"question":
"Product at cathode of dilute H₂SO₄?",

"options":
["Hydrogen","Oxygen"],

"answer":
"Hydrogen",

"hint":
"Hydrogen forms in dilute acids"

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

st.sidebar.metric("Lab",
st.session_state.lab)

# PROGRESS MAP

st.subheader("Lab Progress")

cols=st.columns(5)

for i in range(1,6):

    if i<st.session_state.lab:

        cols[i-1].success(
        "Lab "+str(i))

    elif i==st.session_state.lab:

        cols[i-1].info(
        "Lab "+str(i))

    else:

        cols[i-1].write(
        "🔒 Lab "+str(i))

# GAME CARD

st.subheader(
"Lab "+str(st.session_state.lab)+ ": "+lab["name"])

st.info(lab["question"])

choice=st.radio(

"Choose",

lab["options"])

col1,col2=st.columns(2)

with col1:

    if st.button("Submit"):

        st.session_state.answered=True

        if choice==lab["answer"]:

            st.success("Correct")

            st.balloons()

            st.session_state.xp+=20

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

    if st.button("Next Lab"):

        if st.session_state.lab<5:

            st.session_state.lab+=1

        st.session_state.answered=False

        st.rerun()

# PROGRESS BAR

st.subheader(
"Mastery Progress")

st.progress(
min(
st.session_state.xp/150,
1.0))

# ACHIEVEMENTS

st.subheader("Achievements")

if st.session_state.stars>=3:

    st.write("⭐ Ion Explorer")

if st.session_state.stars>=5:

    st.write("⚡ Lab Technician")

if st.session_state.stars>=8:

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

with st.expander(
"Review concept"):

    st.write(lab["hint"])
