import streamlit as st
import time

st.set_page_config(page_title="Electrolysis Quest", layout="wide")

# --- PLAYER STATE ---
state_keys = {
    "xp": 0, "lab": 1, "lives": 5, "stars": 0, 
    "streak": 0, "lab_question": 0, "answered": False
}
for key, value in state_keys.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- FULL LAB DATA BANK ---
labs = {
    1: {
        "name": "Electrolysis Foundations",
        "questions": [
            {"type": "placement", "question": "Set up the cell: Place Na⁺ and Cl⁻", "ions": [("Na⁺", "Cathode"), ("Cl⁻", "Anode")], "hint": "PANIC: Positive Anode, Negative Is Cathode. Cations (Na⁺) go to the Cathode."},
            {"type": "placement", "question": "Set up the cell: Place K⁺ and Br⁻", "ions": [("K⁺", "Cathode"), ("Br⁻", "Anode")], "hint": "Cations move to the negative electrode (Cathode)."},
            {"type": "mcq", "question": "Which electrode is positive?", "options": ["Cathode", "Anode", "Electrolyte", "Wire"], "answer": "Anode", "hint": "Oxidation occurs there (An-Ox)."},
            {"type": "mcq", "question": "Which is a cation?", "options": ["Cl⁻", "SO₄²⁻", "Na⁺", "OH⁻"], "answer": "Na⁺", "hint": "Cations are positive ions."},
            {"type": "mcq", "question": "Which process occurs at the cathode?", "options": ["Oxidation", "Reduction", "Heating", "Neutralisation"], "answer": "Reduction", "hint": "Gain of electrons (Red-Cat)."}
        ]
    },
    2: {
        "name": "Products of Electrolysis",
        "questions": [
            {"type": "mcq", "question": "Product at cathode in dilute acid?", "options": ["Oxygen", "Hydrogen", "Sulfur", "Water"], "answer": "Hydrogen", "hint": "H⁺ ions gain electrons at the cathode."},
            {"type": "mcq", "question": "Product at cathode in CuSO₄ (aq)?", "options": ["Copper", "Hydrogen", "Oxygen", "Sulfur"], "answer": "Copper", "hint": "Less reactive metals deposit first."},
            {"type": "mcq", "question": "Product at anode in concentrated brine?", "options": ["Hydrogen", "Sodium", "Chlorine", "Copper"], "answer": "Chlorine", "hint": "High concentration of Cl⁻ leads to its discharge."},
            {"type": "mcq", "question": "Gas produced at the anode during water electrolysis?", "options": ["Hydrogen", "Oxygen", "Nitrogen", "Chlorine"], "answer": "Oxygen", "hint": "OH⁻ ions form oxygen and water."},
            {"type": "mcq", "question": "What happens to the cathode in CuSO₄ electrolysis?", "options": ["Gets thinner", "Gets coated", "No change", "Breaks"], "answer": "Gets coated", "hint": "Copper metal deposits on the surface."}
        ]
    },
    3: {
        "name": "Discharge Factors",
        "questions": [
            {"type": "mcq", "question": "Why does hydrogen form instead of sodium in aqueous solutions?", "options": ["Inactive", "Easier reduction", "Disappears", "No reason"], "answer": "Easier reduction", "hint": "Check the reactivity series; H is below Na."},
            {"type": "mcq", "question": "What is the main factor for ion discharge?", "options": ["Colour", "Electrochemical Series", "Shape", "Light"], "answer": "Electrochemical Series", "hint": "Position in the series determines ease of discharge."},
            {"type": "mcq", "question": "Which factor affects the product at the anode in NaCl?", "options": ["Concentration", "Bottle size", "Wire colour", "Room temp"], "answer": "Concentration", "hint": "Concentrated Cl⁻ wins over OH⁻."},
            {"type": "mcq", "question": "The type of electrode used affects?", "options": ["Voltage", "Products", "Colour", "Shape"], "answer": "Products", "hint": "Active electrodes (like Cu) can participate in the reaction."},
            {"type": "mcq", "question": "Which ion discharges first: Cu²⁺ or H⁺?", "options": ["Cu²⁺", "H⁺"], "answer": "Cu²⁺", "hint": "Copper is lower in the electrochemical series."}
        ]
    },
    4: {
        "name": "Industrial Applications",
        "questions": [
            {"type": "mcq", "question": "What is the main purpose of electroplating?", "options": ["Destroy", "Coat/Protect", "Melt", "Clean"], "answer": "Coat/Protect", "hint": "Creating a protective or decorative layer."},
            {"type": "mcq", "question": "The object to be plated is always the:", "options": ["Anode", "Cathode", "Electrolyte", "Cell"], "answer": "Cathode", "hint": "Metal ions move toward the negative electrode to deposit."},
            {"type": "mcq", "question": "Electrolysis is industrially used for:", "options": ["Cooking", "Aluminium extraction", "Boiling", "Freezing"], "answer": "Aluminium extraction", "hint": "The Hall-Héroult process."},
            {"type": "mcq", "question": "During copper purification, pure copper forms at the:", "options": ["Cathode", "Anode", "Wire", "Switch"], "answer": "Cathode", "hint": "The impure anode dissolves and pure metal deposits at the cathode."},
            {"type": "mcq", "question": "Electrolysis primarily produces:", "options": ["Electricity", "Chemicals", "Sand", "Heat"], "answer": "Chemicals", "hint": "It converts electrical energy into chemical energy."}
        ]
    },
    5: {
        "name": "WAEC Challenge",
        "questions": [
            {"type": "mcq", "question": "Product at cathode in molten NaCl?", "options": ["Sodium", "Hydrogen", "Chlorine", "Oxygen"], "answer": "Sodium", "hint": "In 'molten' state, there is no water/hydrogen to compete."},
            {"type": "mcq", "question": "Product at cathode in aqueous NaCl?", "options": ["Sodium", "Hydrogen", "Chlorine", "Oxygen"], "answer": "Hydrogen", "hint": "Water is present; H⁺ discharges more easily than Na⁺."},
            {"type": "mcq", "question": "Why does chlorine form in concentrated NaCl?", "options": ["Colour", "High chloride concentration", "Heat", "Glass"], "answer": "High chloride concentration", "hint": "The concentration effect overrides the electrochemical series here."},
            {"type": "mcq", "question": "Which species loses electrons during electrolysis?", "options": ["Cation", "Anion", "Metal", "Water"], "answer": "Anion", "hint": "Anions move to the anode to undergo oxidation (loss of electrons)."},
            {"type": "mcq", "question": "Why are inert electrodes like graphite used?", "options": ["Cheap", "Do not react", "Heavy", "Magnetic"], "answer": "Do not react", "hint": "They conduct electricity without participating in the reaction."}
        ]
    }
}

# --- SIDEBAR STATS ---
with st.sidebar:
    st.header("🎮 Player Dashboard")
    st.metric("Total XP", f"{st.session_state.xp} ⚡")
    st.write(f"Health: {'❤️' * st.session_state.lives}")
    st.write(f"Stars Earned: {'⭐' * st.session_state.stars}")
    if st.session_state.streak > 1:
        st.success(f"🔥 {st.session_state.streak}x Answer Streak!")
    st.divider()
    if st.button("Reset Game"):
        for key in state_keys: st.session_state[key] = state_keys[key]
        st.rerun()

# --- GAME ENGINE ---
if st.session_state.lives <= 0:
    st.error("💀 LAB EXPLODED! You ran out of lives.")
    st.stop()

if st.session_state.lab > 5:
    st.balloons()
    st.title("🏆 THE ELECTROLYSIS MASTER")
    st.success(f"Final Score: {st.session_state.xp} XP and {st.session_state.stars} Stars!")
    st.stop()

# Load current context
lab = labs[st.session_state.lab]
question = lab["questions"][st.session_state.lab_question]

st.title("⚡ Electrolysis Quest")
st.subheader(f"Lab {st.session_state.lab}: {lab['name']}")
st.progress(st.session_state.lab_question / 5, text=f"Question {st.session_state.lab_question + 1} of 5")

# --- UI FOR QUESTIONS ---
if question["type"] == "placement":
    st.write(f"### {question['question']}")
    ion_list = [i[0] for i in question["ions"]]
    
    c1, c2 = st.columns(2)
    with c1: anode_sel = st.selectbox("Select ion for Anode (+)", ["Select..."] + ion_list)
    with c2: cathode_sel = st.selectbox("Select ion for Cathode (-)", ["Select..."] + ion_list)
    
    if st.button("Run Experiment", disabled=st.session_state.answered):
        if anode_sel == "Select..." or cathode_sel == "Select...":
            st.warning("Please place ions first!")
        else:
            with st.status("Analyzing Ion Migration..."):
                time.sleep(1.5)
                # Check logic
                correct_count = 0
                for ion, target in question["ions"]:
                    if ion == anode_sel and target == "Anode": correct_count += 1
                    if ion == cathode_sel and target == "Cathode": correct_count += 1
                
                if correct_count == 2:
                    st.session_state.xp += 30
                    st.session_state.streak += 1
                    st.session_state.answered = True
                    st.success("Perfect placement! The cell is working.")
                else:
                    st.session_state.lives -= 1
                    st.session_state.streak = 0
                    st.error("Short circuit! The ions are at the wrong electrodes.")

elif question["type"] == "mcq":
    st.write(f"### {question['question']}")
    user_choice = st.radio("Choose the correct outcome:", question["options"], index=None)
    
    if st.button("Submit Answer", disabled=st.session_state.answered):
        if user_choice == question["answer"]:
            bonus = st.session_state.streak * 5
            st.session_state.xp += (20 + bonus)
            st.session_state.streak += 1
            st.session_state.answered = True
            st.toast(f"Correct! +{20+bonus} XP")
        else:
            st.session_state.lives -= 1
            st.session_state.streak = 0
            st.error("Wrong choice! Check your hint below.")

# --- FOOTER CONTROLS ---
if not st.session_state.answered:
    if st.button("💡 Use Hint (-5 XP)"):
        st.session_state.xp -= 5
        st.info(question["hint"])

if st.session_state.answered:
    if st.button("Next Question ➡️"):
        st.session_state.lab_question += 1
        st.session_state.answered = False
        if st.session_state.lab_question >= 5:
            st.session_state.stars += 1
            st.session_state.lab += 1
            st.session_state.lab_question = 0
            st.balloons()
        st.rerun()
