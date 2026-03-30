import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(page_title="⚡ Electrolysis Quest", layout="wide")

st.title("⚡ Electrolysis Quest – Final Prototype")

# --- SESSION STATE ---
if "xp" not in st.session_state: st.session_state.xp = 0
if "lab" not in st.session_state: st.session_state.lab = 1
if "lives" not in st.session_state: st.session_state.lives = 3
if "stars" not in st.session_state: st.session_state.stars = 0
if "streak" not in st.session_state: st.session_state.streak = 0
if "exam_score" not in st.session_state: st.session_state.exam_score = 0
if "weak_topic" not in st.session_state: st.session_state.weak_topic = "None"
if "exam_started" not in st.session_state: st.session_state.exam_started = False

# --- LOAD QUESTION BANK ---
questions_df = pd.read_csv("questions.csv")  # CSV should have: question,option1,option2,option3,option4,answer,topic,level

# --- PLAYER PANEL ---
st.sidebar.title("Player")
st.sidebar.metric("XP ⚡", st.session_state.xp)
st.sidebar.metric("Lives ❤️", st.session_state.lives)
st.sidebar.metric("Stars ⭐", st.session_state.stars)
st.sidebar.metric("Streak 🔥", st.session_state.streak)

# --- MAIN MENU ---
mode = st.radio("Select Mode", ["Labs", "WAEC Exam", "Performance", "Teacher Dashboard"])

# ---------------- LABS MODE ----------------
if mode == "Labs":
    st.subheader(f"Lab {st.session_state.lab}")

    # Pick questions for current lab level
    lab_questions = questions_df[questions_df["level"]==st.session_state.lab]
    if lab_questions.empty:
        st.info("No questions for this lab level")
    else:
        q = lab_questions.sample(1).iloc[0]
        st.info(f"Topic: {q['topic']}")
        st.write(q["question"])

        choice = st.radio("Select Answer", [q["option1"], q["option2"], q["option3"], q["option4"]])

        if st.button("Submit Answer", key="lab_submit"):
            if choice == q["answer"]:
                st.success("Correct!")
                st.session_state.xp += 20
                st.session_state.stars += 1
                st.session_state.streak += 1
            else:
                st.error(f"Wrong! Hint: {q['topic']}")
                st.session_state.lives -= 1
                st.session_state.streak = 0
                st.session_state.weak_topic = q["topic"]

        if st.button("Next Lab", key="lab_next"):
            st.session_state.lab = min(st.session_state.lab + 1, questions_df["level"].max())
            st.rerun()

# ---------------- WAEC EXAM MODE ----------------
elif mode == "WAEC Exam":
    st.subheader("WAEC Practice Test – 20 Questions")
    
    if not st.session_state.exam_started:
        st.session_state.exam_questions = questions_df.sample(20)
        st.session_state.exam_started = True
        st.session_state.exam_answers = [None]*20
        st.session_state.exam_timer = 300  # 5 min total

    for i, row in st.session_state.exam_questions.iterrows():
        st.write(f"Q{i+1}: {row['question']}")
        ans = st.radio("", [row["option1"], row["option2"], row["option3"], row["option4"]],
                       key=f"exam_{i}")
        st.session_state.exam_answers[i] = ans

    if st.button("Submit Exam"):
        score = 0
        weak_topics = []
        for ans, row in zip(st.session_state.exam_answers, st.session_state.exam_questions.itertuples()):
            if ans == row.answer:
                score += 1
            else:
                weak_topics.append(row.topic)
        st.session_state.exam_score = score
        if weak_topics:
            st.session_state.weak_topic = random.choice(weak_topics)
        st.success(f"Score: {score}/20")
        st.session_state.exam_started = False

# ---------------- PERFORMANCE ----------------
elif mode == "Performance":
    st.subheader("Performance Report")
    st.metric("Exam Score", st.session_state.exam_score)
    st.metric("XP", st.session_state.xp)
    st.metric("Stars", st.session_state.stars)
    st.metric("Streak", st.session_state.streak)
    st.metric("Weak Topic", st.session_state.weak_topic)

    if st.session_state.weak_topic != "None":
        st.warning(f"Focus on: {st.session_state.weak_topic}")

# ---------------- TEACHER DASHBOARD ----------------
elif mode == "Teacher Dashboard":
    st.subheader("Teacher Dashboard")
    st.write("Student performance overview (simulated for prototype)")
    st.write(f"XP: {st.session_state.xp}")
    st.write(f"Stars: {st.session_state.stars}")
    st.write(f"Weak Topic: {st.session_state.weak_topic}")
    st.write(f"Lives: {st.session_state.lives}")
    st.write(f"Lab Level: {st.session_state.lab}")

# ---------------- GAME OVER ----------------
if st.session_state.lives <= 0:
    st.error("Game Over! 😢")
    if st.button("Restart Game"):
        st.session_state.xp = 0
        st.session_state.lab = 1
        st.session_state.lives = 3
        st.session_state.stars = 0
        st.session_state.streak = 0
        st.session_state.exam_score = 0
        st.session_state.weak_topic = "None"
        st.session_state.exam_started = False
        st.rerun()
