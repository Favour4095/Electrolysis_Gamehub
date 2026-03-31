import streamlit as st
import time
import random

st.set_page_config(layout="wide")
st.title("⚡ Electrolysis Quest – Virtual Lab")

# ----------------------------
# PLAYER STATE
# ----------------------------
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "lives" not in st.session_state:
    st.session_state.lives = 3
if "stars" not in st.session_state:
    st.session_state.stars = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "lab" not in st.session_state:
    st.session_state.lab = 1
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "lab_start_time" not in st.session_state:
    st.session_state.lab_start_time = time.time()

# ----------------------------
# LAB QUESTIONS BANK
# ----------------------------
labs = {
    1: [
        {"question": "Which ion moves to the cathode?", "options": ["Na⁺", "Cl⁻", "H⁺", "OH⁻"], "answer": "Na⁺", "hint": "Positive ions move to cathode."},
        {"question": "Which ion moves to the anode?", "options": ["Na⁺", "Cl⁻", "H⁺", "OH⁻"], "answer": "Cl⁻", "hint": "Negative ions move to anode."},
        {"question": "Oxidation occurs at?", "options": ["Cathode", "Anode", "Electrolyte", "Both"], "answer": "Anode", "hint": "Anode loses electrons."},
        {"question": "Reduction occurs at?", "options": ["Cathode", "Anode", "Electrolyte", "Both"], "answer": "Cathode", "hint": "Cathode gains electrons."},
        {"question": "Positive ions gain electrons?", "options": ["Yes", "No"], "answer": "Yes", "hint": "Positive ions are reduced."}
    ],
    2: [
        {"question": "Which ion moves to the cathode?", "options": ["Cu²⁺", "SO₄²⁻", "H⁺", "Cl⁻"], "answer": "Cu²⁺", "hint": "Metal cations move to cathode."},
        {"question": "Which ion moves to the anode?", "options": ["Cu²⁺", "SO₄²⁻", "H⁺", "Cl⁻"], "answer": "SO₄²⁻", "hint": "Anions go to anode."},
        {"question": "Oxidation at anode is?", "options": ["Cu", "SO₄", "Electron gain", "Electron loss"], "answer": "Electron loss", "hint": "Anode loses electrons."},
        {"question": "Reduction at cathode is?", "options": ["Cu", "SO₄", "Electron gain", "Electron loss"], "answer": "Electron gain", "hint": "Cathode gains electrons."},
        {"question": "Electrolyte used?", "options": ["NaCl", "CuSO₄", "H₂SO₄", "NaOH"], "answer": "CuSO₄", "hint": "Copper sulfate solution."}
    ],
    3: [
        {"question": "Ion at cathode in acid?", "options": ["H⁺", "SO₄²⁻", "OH⁻", "Na⁺"], "answer": "H⁺", "hint": "Hydrogen ions are reduced."},
        {"question": "Ion at anode in acid?", "options": ["H⁺", "SO₄²⁻", "OH⁻", "Cl⁻"], "answer": "SO₄²⁻", "hint": "Anions oxidized."},
        {"question": "Electrolyte is?", "options": ["H₂SO₄", "NaCl", "CuSO₄", "NaOH"], "answer": "H₂SO₄", "hint": "Dilute sulfuric acid."},
        {"question": "Oxidation involves?", "options": ["Electron gain", "Electron loss"], "answer": "Electron loss", "hint": "Anode loses electrons."},
        {"question": "Reduction involves?", "options": ["Electron gain", "Electron loss"], "answer": "Electron gain", "hint": "Cathode gains electrons."}
    ],
    4: [
        {"question": "Ion moving to cathode in brine?", "options": ["H⁺", "Cl⁻", "Na⁺", "OH⁻"], "answer": "H⁺", "hint": "Hydrogen ions reduced at cathode."},
        {"question": "Ion moving to anode in brine?", "options": ["H⁺", "Cl⁻", "Na⁺", "OH⁻"], "answer": "Cl⁻", "hint": "Chloride ions oxidized."},
        {"question": "Brine is?", "options": ["NaCl(aq)", "CuSO₄", "H₂SO₄", "NaOH"], "answer": "NaCl(aq)", "hint": "Saturated salt solution."},
        {"question": "At anode oxidation?", "options": ["Cl⁻ → Cl₂", "Na⁺ → Na"], "answer": "Cl⁻ → Cl₂", "hint": "Chloride ions form chlorine gas."},
        {"question": "At cathode reduction?", "options": ["H⁺ → H₂", "Na⁺ → Na"], "answer": "H⁺ → H₂", "hint": "Hydrogen gas released."}
    ],
    5: [
        {"question": "Cu²⁺ moves to?", "options": ["Cathode", "Anode"], "answer": "Cathode", "hint": "Metal cations move to cathode."},
        {"question": "Cl⁻ moves to?", "options": ["Cathode", "Anode"], "answer": "Anode", "hint": "Anions go to anode."},
        {"question": "Electrolyte in WAEC challenge?", "options": ["Mixed Cell", "H₂SO₄", "NaCl", "CuSO₄"], "answer": "Mixed Cell", "hint": "Mixed ions present."},
        {"question": "Oxidation site?", "options": ["Anode", "Cathode"], "answer": "Anode", "hint": "Anode loses electrons."},
        {"question": "Reduction site?", "options": ["Cathode", "Anode"], "answer": "Cathode", "hint": "Cathode gains electrons."}
    ]
}

lab_questions = labs[st.session_state.lab]
q_index = st.session_state.question_index
question = lab_questions[q_index]

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.title("Player Stats")
st.sidebar.metric("XP ⚡", st.session_state.xp)
st.sidebar.metric("Lives ❤️", st.session_state.lives)
st.sidebar.metric("Stars ⭐", st.session_state.stars)
st.sidebar.metric("Streak 🔥", st.session_state.streak)

# ----------------------------
# COUNTDOWN TIMER
# ----------------------------
timer_placeholder = st.empty()
elapsed = time.time() - st.session_state.lab_start_time
remaining = max(300 - int(elapsed), 0)
minutes = remaining // 60
seconds = remaining % 60
timer_placeholder.metric("⏱ Time Left", f"{minutes:02d}:{seconds:02d}")

if remaining == 0:
    st.error("⏰ Time's up! Life deducted.")
    st.session_state.lives -= 1
    st.session_state.lab_start_time = time.time()
    st.experimental_rerun()

# ----------------------------
# QUESTION DISPLAY
# ----------------------------
st.subheader(f"Lab {st.session_state.lab} – Question {q_index+1}")
st.write(question["question"])
selected = st.radio("Select Answer", question["options"])

# HINT
if st.button("Hint 💡"):
    st.warning(question["hint"])
    st.session_state.xp = max(st.session_state.xp-5, 0)

# ----------------------------
# NAVIGATION BUTTONS
# ----------------------------
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅ Previous Question") and q_index > 0:
        st.session_state.question_index -= 1
        st.experimental_rerun()
with col2:
    if st.button("Submit Answer"):
        if selected == question["answer"]:
            st.success("✅ Correct!")
            st.session_state.xp += 10
            st.session_state.stars += 1
            st.session_state.streak += 1
        else:
            st.error(f"❌ Wrong! Correct answer: {question['answer']}")
            st.session_state.lives -= 1
            st.session_state.streak = 0
with col3:
    if st.button("Next Question ➡"):
        if q_index < len(lab_questions)-1:
            st.session_state.question_index += 1
        else:
            st.success("🎉 Lab Completed!")
            if st.button("Next Level 🚀"):
                st.session_state.lab += 1
                st.session_state.question_index = 0
                st.session_state.lab_start_time = time.time()
        st.experimental_rerun()

# ----------------------------
# ACHIEVEMENTS / BADGES
# ----------------------------
st.subheader("Badges 🏅")
if st.session_state.stars >= 5:
    st.write("⭐ Ion Handler")
if st.session_state.stars >= 10:
    st.write("⚡ Lab Expert")
if st.session_state.stars >= 15:
    st.write("🏆 Electrolysis Master")

# ----------------------------
# GAME OVER
# ----------------------------
if st.session_state.lives <= 0:
    st.error("💀 Game Over")
    if st.button("Restart Game 🔄"):
        for key in ["xp","lives","stars","streak","lab","question_index","lab_start_time"]:
            st.session_state[key] = 0 if key in ["xp","stars","streak","question_index"] else 1 if key=="lab" else 3
        st.session_state.lab_start_time = time.time()
        st.experimental_rerun()
