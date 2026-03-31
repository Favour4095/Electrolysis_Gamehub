import streamlit as st
import time
import random

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Electrolysis Quest Pro", page_icon="⚡", layout="wide")

# 2. CUSTOM CSS (Inspired by Periodic Master)
st.markdown("""
<style>
@keyframes backgroundAnimation { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
.stApp {
    background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e);
    background-size: 400% 400%;
    animation: backgroundAnimation 20s ease infinite;
}
.stExpander, .instruction-box, .stChatMessage, .stSelectbox {
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}
h1, h2, h3, h4, p, label, .stMarkdown { color: #e0e0e0 !important; }
.main-title { text-align: center; color: #4facfe !important; font-size: 40px; font-weight: 800; text-shadow: 0 0 15px #4facfe; }
.stMetric { background: rgba(0, 0, 0, 0.2); padding: 10px; border-radius: 10px; border-left: 5px solid #4facfe; }
.stButton>button { 
    background: linear-gradient(45deg, #4facfe, #00f2fe); 
    color: white; border-radius: 10px; font-weight: bold; width: 100%; 
    transition: 0.3s; border: none;
}
.stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #4facfe; }
</style>
""", unsafe_allow_html=True)

# 3. PLAYER STATE MANAGEMENT
state_keys = {
    "xp": 0, "lab": 1, "lives": 5, "stars": 0, 
    "streak": 0, "lab_question": 0, "answered": False, "mode": "play"
}
for key, value in state_keys.items():
    if key not in st.session_state:
        st.session_state[key] = value

# 4. FULL LAB DATA BANK
labs = {
    1: {"name": "Electrolysis Foundations", "questions": [
        {"type": "placement", "question": "Place Na⁺ and Cl⁻", "ions": [("Na⁺", "Cathode"), ("Cl⁻", "Anode")], "hint": "Cations move to the negative cathode."},
        {"type": "placement", "question": "Place K⁺ and Br⁻", "ions": [("K⁺", "Cathode"), ("Br⁻", "Anode")], "hint": "Positive ions go to cathode."},
        {"type": "mcq", "question": "Which electrode is positive?", "options": ["Cathode", "Anode", "Electrolyte", "Wire"], "answer": "Anode", "hint": "An-Ox: Oxidation at Anode."},
        {"type": "mcq", "question": "Which is a cation?", "options": ["Cl⁻", "SO₄²⁻", "Na⁺", "OH⁻"], "answer": "Na⁺", "hint": "Cations are positive."},
        {"type": "mcq", "question": "Which occurs at cathode?", "options": ["Oxidation", "Reduction", "Heating", "Neutralisation"], "answer": "Reduction", "hint": "Red-Cat: Reduction at Cathode."}
    ]},
    2: {"name": "Products", "questions": [
        {"type": "mcq", "question": "Product at cathode in dilute acid?", "options": ["Oxygen", "Hydrogen", "Sulfur", "Water"], "answer": "Hydrogen", "hint": "H⁺ gains electrons."},
        {"type": "mcq", "question": "Product at cathode in CuSO₄?", "options": ["Copper", "Hydrogen", "Oxygen", "Sulfur"], "answer": "Copper", "hint": "Less reactive metal deposits."},
        {"type": "mcq", "question": "Product at anode in brine?", "options": ["Hydrogen", "Sodium", "Chlorine", "Copper"], "answer": "Chlorine", "hint": "Cl⁻ loses electrons."},
        {"type": "mcq", "question": "Gas at anode in water electrolysis?", "options": ["Hydrogen", "Oxygen", "Nitrogen", "Chlorine"], "answer": "Oxygen", "hint": "OH⁻ forms oxygen."},
        {"type": "mcq", "question": "What happens to CuSO₄ cathode?", "options": ["Gets thinner", "Gets coated", "No change", "Breaks"], "answer": "Gets coated", "hint": "Copper deposits."}
    ]},
    3: {"name": "Discharge Factors", "questions": [
        {"type": "mcq", "question": "Why hydrogen forms instead of sodium?", "options": ["Inactive", "Easier reduction", "Disappears", "No reason"], "answer": "Easier reduction", "hint": "Reactivity series."},
        {"type": "mcq", "question": "Main discharge factor?", "options": ["Colour", "Series", "Shape", "Light"], "answer": "Series", "hint": "Electrochemical series."},
        {"type": "mcq", "question": "Which affects product?", "options": ["Concentration", "Bottle", "Wire colour", "Room"], "answer": "Concentration", "hint": "More ions discharge."},
        {"type": "mcq", "question": "Electrode type affects?", "options": ["Voltage", "Products", "Colour", "Shape"], "answer": "Products", "hint": "Active electrodes react."},
        {"type": "mcq", "question": "Which discharges first?", "options": ["Cu²⁺", "H⁺"], "answer": "Cu²⁺", "hint": "Copper below hydrogen."}
    ]},
    4: {"name": "Applications", "questions": [
        {"type": "mcq", "question": "Electroplating purpose?", "options": ["Destroy", "Coat", "Melt", "Clean"], "answer": "Coat", "hint": "Protective layer."},
        {"type": "mcq", "question": "Object plated is?", "options": ["Anode", "Cathode", "Electrolyte", "Cell"], "answer": "Cathode", "hint": "Metal deposits there."},
        {"type": "mcq", "question": "Electrolysis used for?", "options": ["Cooking", "Aluminium extraction", "Boiling", "Freezing"], "answer": "Aluminium extraction", "hint": "Bauxite process."},
        {"type": "mcq", "question": "Pure copper forms at?", "options": ["Cathode", "Anode", "Wire", "Switch"], "answer": "Cathode", "hint": "Purification."},
        {"type": "mcq", "question": "Electrolysis produces?", "options": ["Electricity", "Chemicals", "Sand", "Heat"], "answer": "Chemicals", "hint": "Industrial use."}
    ]},
    5: {"name": "WAEC Challenge", "questions": [
        {"type": "mcq", "question": "Product at cathode molten NaCl?", "options": ["Sodium", "Hydrogen", "Chlorine", "Oxygen"], "answer": "Sodium", "hint": "No water present."},
        {"type": "mcq", "question": "Product cathode aqueous NaCl?", "options": ["Sodium", "Hydrogen", "Chlorine", "Oxygen"], "answer": "Hydrogen", "hint": "Water competes."},
        {"type": "mcq", "question": "Why chlorine forms?", "options": ["Colour", "High chloride", "Heat", "Glass"], "answer": "High chloride", "hint": "Concentration effect."},
        {"type": "mcq", "question": "Which loses electrons?", "options": ["Cation", "Anion", "Metal", "Water"], "answer": "Anion", "hint": "Oxidation."},
        {"type": "mcq", "question": "Why inert electrodes?", "options": ["Cheap", "Do not react", "Heavy", "Magnetic"], "answer": "Do not react", "hint": "Graphite."}
    ]}
}

# --- HEADER DASHBOARD ---
st.markdown('<h1 class="main-title">🛡️ Electrolysis Quest: Lab Master</h1>', unsafe_allow_html=True)

d1, d2, d3, d4 = st.columns(4)
with d1: st.metric("LEVEL", f"Lab {st.session_state.lab}")
with d2: st.metric("XP POINTS", f"{st.session_state.xp} ⚡")
with d3: st.metric("STREAK", f"{st.session_state.streak} 🔥")
with d4: st.metric("HEALTH", "❤️" * st.session_state.lives)

st.divider()

# --- GAME OVER / COMPLETE CHECK ---
if st.session_state.lives <= 0:
    st.error("💀 EXPERIMENT FAILED: Equipment Damaged. Your journey ends here.")
    if st.button("🔄 Restart Quest"):
        for key in state_keys: st.session_state[key] = state_keys[key]
        st.rerun()
    st.stop()

if st.session_state.lab > 5:
    st.balloons()
    st.markdown("<h2 style='text-align:center;'>🏆 THE DIGITAL TEACHER CERTIFIED MASTER</h2>", unsafe_allow_html=True)
    st.success(f"Final Score: {st.session_state.xp} XP | Stars: {st.session_state.stars}")
    if st.button("Restart Journey"):
        for key in state_keys: st.session_state[key] = state_keys[key]
        st.rerun()
    st.stop()

# --- MAIN UI LOGIC ---
lab_data = labs[st.session_state.lab]
question = lab_data["questions"][st.session_state.lab_question]

col_a, col_b = st.columns([2, 1])

with col_a:
    st.subheader(f"📍 Current Goal: {lab_data['name']}")
    st.progress(st.session_state.lab_question / 5, text=f"Question {st.session_state.lab_question+1}/5")
    
    # QUESTION ENGINE
    if question["type"] == "placement":
        st.info(f"🧪 **Virtual Lab Task:** {question['question']}")
        ion_list = [i[0] for i in question["ions"]]
        c1, c2 = st.columns(2)
        with c1: anode_sel = st.selectbox("Anode (+)", ["---"] + ion_list)
        with c2: cathode_sel = st.selectbox("Cathode (-)", ["---"] + ion_list)

        if st.button("🚀 Run Experiment", disabled=st.session_state.answered):
            if anode_sel == "---" or cathode_sel == "---":
                st.warning("Setup the cell first!")
            else:
                with st.status("Analyzing Reaction...") as status:
                    time.sleep(2)
                    correct_count = 0
                    for ion, target in question["ions"]:
                        if ion == anode_sel and target == "Anode": correct_count += 1
                        if ion == cathode_sel and target == "Cathode": correct_count += 1
                    
                    if correct_count == 2:
                        status.update(label="✅ Success! Voltage Stable.", state="complete")
                        st.session_state.xp += 30
                        st.session_state.streak += 1
                        st.session_state.answered = True
                    else:
                        status.update(label="❌ Failure! Short Circuit.", state="error")
                        st.session_state.lives -= 1
                        st.session_state.streak = 0

    elif question["type"] == "mcq":
        st.info(f"❓ **Challenge:** {question['question']}")
        ans = st.radio("Predict Outcome:", question["options"], index=None)
        
        if st.button("SUBMIT ANSWER", disabled=st.session_state.answered):
            if ans == question["answer"]:
                st.toast("Correct! +20 XP")
                st.session_state.xp += 20 + (st.session_state.streak * 5)
                st.session_state.streak += 1
                st.session_state.answered = True
                st.balloons()
            else:
                st.error("Incorrect Prediction!")
                st.session_state.lives -= 1
                st.session_state.streak = 0

with col_b:
    st.markdown("### 🛠️ Lab Tools")
    if st.button("💡 Get Hint (-5 XP)"):
        st.session_state.xp -= 5
        st.warning(question["hint"])
    
    if st.session_state.answered:
        if st.button("Next Stage ➡️"):
            st.session_state.lab_question += 1
            st.session_state.answered = False
            if st.session_state.lab_question >= 5:
                st.session_state.lab += 1
                st.session_state.lab_question = 0
                st.session_state.stars += 1
            st.rerun()

st.markdown('<div style="text-align:center; padding-top:50px; color:#b8c1ec; font-style:italic;">Electrolysis Quest v2.0 - Designed for Educational Mastery</div>', unsafe_allow_html=True)
