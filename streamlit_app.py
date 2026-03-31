import streamlit as st

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

# LAB QUESTION BANK

labs={

1:{
"name":"Electrolysis Foundations",

"questions":[

{"type":"placement",
"question":"Place Na⁺ and Cl⁻",
"ions":[("Na⁺","Cathode"),("Cl⁻","Anode")],
"hint":"Positive ions go to cathode"},

{"type":"placement",
"question":"Place K⁺ and Br⁻",
"ions":[("K⁺","Cathode"),("Br⁻","Anode")],
"hint":"Cations move to cathode"},

{"type":"mcq",
"question":"Which electrode is positive?",
"options":["Cathode","Anode","Electrolyte","Wire"],
"answer":"Anode",
"hint":"Oxidation occurs there"},

{"type":"mcq",
"question":"Which is a cation?",
"options":["Cl⁻","SO₄²⁻","Na⁺","OH⁻"],
"answer":"Na⁺",
"hint":"Cations are positive"},

{"type":"mcq",
"question":"Which occurs at cathode?",
"options":["Oxidation","Reduction","Heating","Neutralisation"],
"answer":"Reduction",
"hint":"Gain electrons"}

]

},

2:{
"name":"Products",

"questions":[

{"type":"mcq",
"question":"Product at cathode in dilute acid?",
"options":["Oxygen","Hydrogen","Sulfur","Water"],
"answer":"Hydrogen",
"hint":"H⁺ gains electrons"},

{"type":"mcq",
"question":"Product at cathode in CuSO₄?",
"options":["Copper","Hydrogen","Oxygen","Sulfur"],
"answer":"Copper",
"hint":"Less reactive metal deposits"},

{"type":"mcq",
"question":"Product at anode in brine?",
"options":["Hydrogen","Sodium","Chlorine","Copper"],
"answer":"Chlorine",
"hint":"Cl⁻ loses electrons"},

{"type":"mcq",
"question":"Gas at anode in water electrolysis?",
"options":["Hydrogen","Oxygen","Nitrogen","Chlorine"],
"answer":"Oxygen",
"hint":"OH⁻ forms oxygen"},

{"type":"mcq",
"question":"What happens to CuSO₄ cathode?",
"options":["Gets thinner","Gets coated","No change","Breaks"],
"answer":"Gets coated",
"hint":"Copper deposits"}

]

},

3:{
"name":"Discharge Factors",

"questions":[

{"type":"mcq",
"question":"Why hydrogen forms instead of sodium?",
"options":["Inactive","Easier reduction","Disappears","No reason"],
"answer":"Easier reduction",
"hint":"Reactivity series"},

{"type":"mcq",
"question":"Main discharge factor?",
"options":["Colour","Series","Shape","Light"],
"answer":"Series",
"hint":"Electrochemical series"},

{"type":"mcq",
"question":"Which affects product?",
"options":["Concentration","Bottle","Wire colour","Room"],
"answer":"Concentration",
"hint":"More ions discharge"},

{"type":"mcq",
"question":"Electrode type affects?",
"options":["Voltage","Products","Colour","Shape"],
"answer":"Products",
"hint":"Active electrodes react"},

{"type":"mcq",
"question":"Which discharges first?",
"options":["Cu²⁺","H⁺"],
"answer":"Cu²⁺",
"hint":"Copper below hydrogen"}

]

},

4:{
"name":"Applications",

"questions":[

{"type":"mcq",
"question":"Electroplating purpose?",
"options":["Destroy","Coat","Melt","Clean"],
"answer":"Coat",
"hint":"Protective layer"},

{"type":"mcq",
"question":"Object plated is?",
"options":["Anode","Cathode","Electrolyte","Cell"],
"answer":"Cathode",
"hint":"Metal deposits there"},

{"type":"mcq",
"question":"Electrolysis used for?",
"options":["Cooking","Aluminium extraction","Boiling","Freezing"],
"answer":"Aluminium extraction",
"hint":"Bauxite process"},

{"type":"mcq",
"question":"Pure copper forms at?",
"options":["Cathode","Anode","Wire","Switch"],
"answer":"Cathode",
"hint":"Purification"},

{"type":"mcq",
"question":"Electrolysis produces?",
"options":["Electricity","Chemicals","Sand","Heat"],
"answer":"Chemicals",
"hint":"Industrial use"}

]

},

5:{
"name":"WAEC Challenge",

"questions":[

{"type":"mcq",
"question":"Product at cathode molten NaCl?",
"options":["Sodium","Hydrogen","Chlorine","Oxygen"],
"answer":"Sodium",
"hint":"No water present"},

{"type":"mcq",
"question":"Product cathode aqueous NaCl?",
"options":["Sodium","Hydrogen","Chlorine","Oxygen"],
"answer":"Hydrogen",
"hint":"Water competes"},

{"type":"mcq",
"question":"Why chlorine forms?",
"options":["Colour","High chloride","Heat","Glass"],
"answer":"High chloride",
"hint":"Concentration effect"},

{"type":"mcq",
"question":"Which loses electrons?",
"options":["Cation","Anion","Metal","Water"],
"answer":"Anion",
"hint":"Oxidation"},

{"type":"mcq",
"question":"Why inert electrodes?",
"options":["Cheap","Do not react","Heavy","Magnetic"],
"answer":"Do not react",
"hint":"Graphite"}

]

}

}

lab=labs[st.session_state.lab]

question=lab["questions"][st.session_state.lab_question]

# PLAYER PANEL

st.sidebar.metric("XP ⚡",st.session_state.xp)
st.sidebar.metric("Lives ❤️",st.session_state.lives)
st.sidebar.metric("Stars ⭐",st.session_state.stars)

# LAB HEADER

st.subheader("Lab "+str(st.session_state.lab)+" : "+lab["name"])

st.write(
"Question",
st.session_state.lab_question+1,
"/5"
)

# QUESTION ENGINE

if question["type"]=="placement":

    st.write(question["question"])

    ions=[i[0] for i in question["ions"]]

    col1,col2=st.columns(2)

    with col1:
        anode=st.selectbox("Anode",ions)

    with col2:
        cathode=st.selectbox("Cathode",ions)

    if st.button("Run Experiment"):

        correct=0

        for ion in question["ions"]:

            if ion[0]==anode and ion[1]=="Anode":
                correct+=1

            if ion[0]==cathode and ion[1]=="Cathode":
                correct+=1

        if correct==2:

            st.success("Correct")

            st.session_state.xp+=20

            st.session_state.answered=True

        else:

            st.error("Wrong")

            st.session_state.lives-=1

# MCQ ENGINE

if question["type"]=="mcq":

    answer=st.radio(
    question["question"],
    question["options"])

    if st.button("Submit Answer"):

        if answer==question["answer"]:

            st.success("Correct")

            st.balloons()

            st.session_state.xp+=20

            st.session_state.streak+=1

            st.session_state.answered=True

        else:

            st.error("Wrong")

            st.session_state.lives-=1

            st.session_state.streak=0

# HINT

if st.button("💡 Hint"):

    st.info(question["hint"])

# NEXT

if st.button("Next Question"):

    if st.session_state.answered:

        st.session_state.lab_question+=1

        st.session_state.answered=False

        if st.session_state.lab_question>=5:

            st.success("Lab Completed!")

            st.session_state.xp+=50

            st.session_state.stars+=1

            st.session_state.lab+=1

            st.session_state.lab_question=0

        st.rerun()

    else:

        st.warning("Answer first")

# GAME OVER

if st.session_state.lives<=0:

    st.error("Game Over")

# GAME COMPLETE

if st.session_state.lab>5:

    st.success("🏆 Electrolysis Master")

    st.balloons()
