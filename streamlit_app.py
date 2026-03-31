import streamlit as st
import time
import random

st.set_page_config(layout="wide")
st.title("⚡ Electrolysis Quest – Virtual Lab")

# -----------------------
# PLAYER STATE
# -----------------------
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
if "lab_start_time" not in st.session_state:
    st.session_state.lab_start_time = time.time()
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

# -----------------------
# LAB DATA (5 labs × 5 questions)
# -----------------------
labs = {
    1: {
        "name": "Ion Movement",
        "electrolyte": "NaCl",
        "questions": [
            {"question": "Which ion moves to the cathode?", "options":["Na⁺","Cl⁻"], "answer":"Na⁺", "hint":"Positive ions go to negative electrode"},
            {"question": "Which ion moves to the anode?", "options":["Na⁺","Cl⁻"], "answer":"Cl⁻", "hint":"Negative ions go to positive electrode"},
            {"question": "What happens at the cathode?", "options":["Oxidation","Reduction"], "answer":"Reduction", "hint":"Cathode is negative"},
            {"question": "What happens at the anode?", "options":["Oxidation","Reduction"], "answer":"Oxidation", "hint":"Anode is positive"},
            {"question": "Which gas is released at anode?", "options":["Hydrogen","Chlorine"], "answer":"Chlorine", "hint":"Cl⁻ loses electrons"}
        ]
    },
    2: {
        "name": "Copper Sulphate",
        "electrolyte": "CuSO₄",
        "questions": [
            {"question":"Which ion moves to the cathode?","options":["Cu²⁺","SO₄²⁻"],"answer":"Cu²⁺","hint":"Metal ions are reduced at cathode"},
            {"question":"Which ion moves to the anode?","options":["Cu²⁺","SO₄²⁻"],"answer":"SO₄²⁻","hint":"Negative ions go to anode"},
            {"question":"What happens at cathode?","options":["Oxidation","Reduction"],"answer":"Reduction","hint":"Electrons gained"},
            {"question":"What happens at anode?","options":["Oxidation","Reduction"],"answer":"Oxidation","hint":"Electrons lost"},
            {"question":"What is deposited at cathode?","options":["Copper","Sulphur"],"answer":"Copper","hint":"Metal plates out"}
        ]
    },
    3: {
        "name": "Dilute Acid",
        "electrolyte": "H₂SO₄",
        "questions": [
            {"question":"Which ion moves to cathode?","options":["H⁺","SO₄²⁻"],"answer":"H⁺","hint":"Positive ions go to negative electrode"},
            {"question":"Which ion moves to anode?","options":["H⁺","SO₄²⁻"],"answer":"SO₄²⁻","hint":"Negative ions go to positive electrode"},
            {"question":"Gas released at cathode?","options":["H₂","O₂"],"answer":"H₂","hint":"Hydrogen liberated"},
            {"question":"Gas released at anode?","options":["H₂","O₂"],"answer":"O₂","hint":"Oxygen liberated"},
            {"question":"Electrolyte contains?","options":["Acid","Base"],"answer":"Acid","hint":"H₂SO₄ is acidic"}
        ]
    },
    4: {
        "name": "Brine",
        "electrolyte": "NaCl(aq)",
        "questions": [
            {"question":"Ion at cathode?","options":["H⁺","Cl⁻"],"answer":"H⁺","hint":"Hydrogen reduced"},
            {"question":"Ion at anode?","options":["H⁺","Cl⁻"],"answer":"Cl⁻","hint":"Chlorine oxidized"},
            {"question":"Gas at cathode?","options":["H₂","O₂"],"answer":"H₂","hint":"Hydrogen gas forms"},
            {"question":"Gas at anode?","options":["Cl₂","O₂"],"answer":"Cl₂","hint":"Chlorine gas"},
            {"question":"Reaction type?","options":["Electrolysis","Neutralization"],"answer":"Electrolysis","hint":"Electric current splits ions"}
        ]
    },
    5: {
        "name": "WAEC Challenge",
        "electrolyte": "Mixed Cell",
        "questions": [
            {"question":"Ion at cathode?","options":["Cu²⁺","Na⁺"],"answer":"Cu²⁺","hint":"Metal ion reduced"},
            {"question":"Ion at anode?","options":["Cl⁻","SO₄²⁻"],"answer":"Cl⁻","hint":"Halide oxidized"},
            {"question":"What is plated out?","options":["Copper","Sodium"],"answer":"Copper","hint":"Cu²⁺ gains electrons"},
            {"question":"Gas at anode?","options":["Cl₂","O₂"],"answer":"Cl₂","hint":"Chlorine liberated"},
            {"question":"Reaction type?","options":["Electrolysis","Displacement"],"answer":"Electrolysis","hint":"Current splits ions"}
        ]
    }
}

lab = labs[st.session_state.lab]

# -----------------------
# SIDEBAR PLAYER PANEL
# -----------------------
st.sidebar.title("Player Stats")
st.sidebar.metric("XP ⚡", st.session_state.xp)
st.sidebar.metric("Lives ❤️", st.session_state.lives)
st.sidebar.metric("Stars ⭐", st.session_state.stars)
st.sidebar.metric("Streak 🔥", st.session_state.streak)

# -----------------------
# LAB TIMER
# -----------------------
time_elapsed = time.time() - st.session_state.lab_start_time
time_left = max(300 - int(time_elapsed), 0)  # 5 min = 300 sec
minutes = time_left // 60
seconds = time_left % 60
st.subheader(f"⏱ Lab Timer: {minutes:02d}:{seconds:02d}")
st.progress(time_left / 300)

if time_left == 0:
    st.error("⏱ Time's up!")
    st.session_state.lives -= 1
    st.session_state.lab_start_time = time.time()
    st.experimental_rerun()

# -----------------------
# QUESTION DISPLAY
# -----------------------
question_data = lab["questions"][st.session_state.question_index]
st.subheader(f"Lab {st.session_state.lab}: {lab['name']}")
st.info(f"Electrolyte: {lab['electrolyte']}")
st.write(f"Q{st.session_state.question_index + 1}: {question_data['question']}")

selected_option = st.radio("Select your answer:", question_data["options"], key=f"q{st.session_state.question_index}")

# Hint system
if st.button("Show Hint"):
    st.warning(question_data["hint"])
    st.session_state.xp = max(st.session_state.xp - 5, 0)

# -----------------------
# NAVIGATION BUTTONS
# -----------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Previous Question") and st.session_state.question_index > 0:
        st.session_state.question_index -= 1
        st.experimental_rerun()

with col2:
    if st.button("Submit Answer"):
        if selected_option == question_data["answer"]:
            st.success("✅ Correct!")
            st.session_state.xp += 10
            st.session_state.stars += 1
            st.session_state.streak += 1
        else:
            st.error(f"❌ Wrong! Correct answer: {question_data['answer']}")
            st.session_state.lives -= 1
            st.session_state.streak = 0

        # Move to next question
        if st.session_state.question_index < 4:
            st.session_state.question_index += 1
        else:
            st.success("🎉 Lab Completed!")
        st.experimental_rerun()

with col3:
    if st.button("Next Lab") and st.session_state.lab < 5:
        st.session_state.lab += 1
        st.session_state.question_index = 0
        st.session_state.lab_start_time = time.time()
        st.experimental_rerun()

# -----------------------
# ACHIEVEMENTS / BADGES
# -----------------------
st.subheader("Achievements / Badges")
if st.session_state.stars >= 2:
    st.write("⭐ Ion Handler")
if st.session_state.stars >= 5:
    st.write("⚡ Lab Expert")
if st.session_state.stars >= 10:
    st.write("🏆 Electrolysis Master")

# -----------------------
# GAME OVER
# -----------------------
if st.session_state.lives <= 0:
    st.error("💀 Game Over!")
    if st.button("Restart"):
        for key in ["xp","lab","lives","stars","streak","question_index","lab_start_time"]:
            st.session_state[key] = 0 if key != "lab_start_time" else time.time()
        st.session_state.lab = 1
        st.experimental_rerun()
