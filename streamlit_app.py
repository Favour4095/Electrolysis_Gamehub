import streamlit as st
import random
import time

st.set_page_config(layout="wide")
st.title("⚡ Electrolysis Quest – Virtual Lab")

# ---------------------------
# PLAYER STATE
# ---------------------------
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "lab" not in st.session_state:
    st.session_state.lab = 1
if "lives" not in st.session_state:
    st.session_state.lives = 3
if "stars" not in st.session_state:
    st.session_state.stars = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "time_left" not in st.session_state:
    st.session_state.time_left = 300  # 5 minutes per lab
if "badge" not in st.session_state:
    st.session_state.badge = ""

# ---------------------------
# LAB DATA (5 labs × 5 questions)
# ---------------------------
labs = {
    1: {
        "name": "Ion Movement",
        "electrolyte": "NaCl",
        "questions": [
            ("Which ion goes to the cathode?", "Na⁺"),
            ("Which ion goes to the anode?", "Cl⁻"),
            ("What charge does Na⁺ have?", "Positive"),
            ("What charge does Cl⁻ have?", "Negative"),
            ("At which electrode does reduction occur?", "Cathode"),
        ],
    },
    2: {
        "name": "Copper Sulphate",
        "electrolyte": "CuSO₄",
        "questions": [
            ("Ion at cathode?", "Cu²⁺"),
            ("Ion at anode?", "SO₄²⁻"),
            ("Which ion is reduced?", "Cu²⁺"),
            ("Which ion is oxidized?", "SO₄²⁻"),
            ("Electrode where oxidation occurs?", "Anode"),
        ],
    },
    3: {
        "name": "Dilute Acid",
        "electrolyte": "H₂SO₄",
        "questions": [
            ("Ion at cathode?", "H⁺"),
            ("Ion at anode?", "SO₄²⁻"),
            ("Which ion is reduced?", "H⁺"),
            ("Electrode where oxidation occurs?", "Anode"),
            ("Charge of H⁺?", "Positive"),
        ],
    },
    4: {
        "name": "Brine",
        "electrolyte": "NaCl(aq)",
        "questions": [
            ("Ion at cathode?", "H⁺"),
            ("Ion at anode?", "Cl⁻"),
            ("Electrode where reduction occurs?", "Cathode"),
            ("Electrode where oxidation occurs?", "Anode"),
            ("Which ion is positive?", "H⁺"),
        ],
    },
    5: {
        "name": "WAEC Challenge",
        "electrolyte": "Mixed Cell",
        "questions": [
            ("Ion at cathode?", "Cu²⁺"),
            ("Ion at anode?", "Cl⁻"),
            ("Electrode for reduction?", "Cathode"),
            ("Electrode for oxidation?", "Anode"),
            ("Charge of Cl⁻?", "Negative"),
        ],
    },
}

lab = labs[st.session_state.lab]
total_questions = len(lab["questions"])

# ---------------------------
# SIDEBAR PLAYER PANEL
# ---------------------------
st.sidebar.title("Player")
st.sidebar.metric("Energy ⚡", st.session_state.xp)
st.sidebar.metric("Lives ❤️", st.session_state.lives)
st.sidebar.metric("Stars ⭐", st.session_state.stars)
st.sidebar.metric("Streak 🔥", st.session_state.streak)
st.sidebar.metric("Badge 🏅", st.session_state.badge)

# ---------------------------
# LAB PROGRESS
# ---------------------------
st.subheader("Lab Progress")
cols = st.columns(5)
for i in range(1, 6):
    if i < st.session_state.lab:
        cols[i - 1].success("✔")
    elif i == st.session_state.lab:
        cols[i - 1].info("Current")
    else:
        cols[i - 1].write("🔒")

# ---------------------------
# LAB INFO
# ---------------------------
st.subheader(f"Lab {st.session_state.lab}: {lab['name']}")
st.info(f"Electrolyte: {lab['electrolyte']}")

# ---------------------------
# COUNTDOWN TIMER
# ---------------------------
if st.session_state.time_left > 0:
    st.subheader("⏱ Lab Timer")
    st.progress(st.session_state.time_left / 300)
    st.session_state.time_left -= 1
    st.experimental_rerun()
else:
    st.error("⏱ Time's up!")
    st.session_state.lives -= 1
    st.session_state.time_left = 300
    st.experimental_rerun()

# ---------------------------
# CURRENT QUESTION
# ---------------------------
question_text, correct_answer = lab["questions"][st.session_state.current_question]
st.write(f"**Q{st.session_state.current_question+1}: {question_text}**")

answer = st.text_input("Your answer here:")

# ---------------------------
# HINT
# ---------------------------
if st.button("Hint"):
    st.info(f"Hint: The correct answer starts with '{correct_answer[0]}'")
    st.session_state.xp -= 5

# ---------------------------
# SUBMIT ANSWER
# ---------------------------
if st.button("Submit Answer"):
    if answer.strip().lower() == correct_answer.strip().lower():
        st.success("✅ Correct!")
        st.session_state.xp += 10
        st.session_state.stars += 1
        st.session_state.streak += 1
    else:
        st.error(f"❌ Wrong! Correct answer: {correct_answer}")
        st.session_state.lives -= 1
        st.session_state.streak = 0

# ---------------------------
# NEXT / PREVIOUS BUTTONS
# ---------------------------
col1, col2 = st.columns(2)
with col1:
    if st.button("Previous Question") and st.session_state.current_question > 0:
        st.session_state.current_question -= 1
        st.experimental_rerun()
with col2:
    if st.button("Next Question"):
        if st.session_state.current_question < total_questions - 1:
            st.session_state.current_question += 1
        else:
            st.success("🎉 Lab Complete!")
            # Award badge based on streak
            if st.session_state.streak >= 5:
                st.session_state.badge = "Lab Master 🏅"
            st.session_state.lab += 1
            st.session_state.current_question = 0
            st.session_state.time_left = 300
        st.experimental_rerun()

# ---------------------------
# MASTER LEVEL
# ---------------------------
st.subheader("Mastery Level")
st.progress(min(st.session_state.xp / 250, 1.0))

# ---------------------------
# ACHIEVEMENTS
# ---------------------------
st.subheader("Achievements")
if st.session_state.stars >= 2:
    st.write("⭐ Ion Handler")
if st.session_state.stars >= 4:
    st.write("⚡ Lab Expert")
if st.session_state.stars >= 5:
    st.write("🏆 Electrolysis Master")

# ---------------------------
# GAME OVER
# ---------------------------
if st.session_state.lives <= 0:
    st.error("Game Over")
    if st.button("Restart Game"):
        st.session_state.xp = 0
        st.session_state.lab = 1
        st.session_state.lives = 3
        st.session_state.stars = 0
        st.session_state.streak = 0
        st.session_state.current_question = 0
        st.session_state.time_left = 300
        st.session_state.badge = ""
        st.experimental_rerun()
