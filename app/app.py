import streamlit as st
from env.models import Action
from env.complaint_env import ComplaintEnv

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Naarad AI", layout="centered")

# ---------------- AI LOGIC ----------------
def simple_ai_predict(text):
    text = text.lower()

    if any(word in text for word in ["fire", "accident", "emergency"]):
        return "critical"
    elif any(word in text for word in ["water", "electricity", "power"]):
        return "high"
    elif any(word in text for word in ["not working", "delay", "issue"]):
        return "medium"
    else:
        return "low"

# ---------------- DEPARTMENT LOGIC ----------------
def get_department(text):
    text = text.lower()

    if "water" in text:
        return "💧 Water Department"
    elif "electricity" in text or "light" in text:
        return "⚡ Electricity Department"
    elif "garbage" in text:
        return "🗑️ Sanitation Department"
    elif "fire" in text:
        return "🚒 Emergency Services"
    else:
        return "🏛️ General Administration"

# ---------------- DIFFICULTY ----------------
difficulty = st.selectbox("Select Difficulty", ["easy", "medium", "hard"])

# ---------------- SESSION STATE ----------------
if "env" not in st.session_state or st.session_state.get("difficulty") != difficulty:
    st.session_state.env = ComplaintEnv(difficulty)
    st.session_state.state = st.session_state.env.reset()
    st.session_state.score = 0
    st.session_state.done = False
    st.session_state.correct_count = 0
    st.session_state.total_count = 0
    st.session_state.difficulty = difficulty

env = st.session_state.env
state = st.session_state.state

# ---------------- UI ----------------
st.title("🧠 Naarad AI - Complaint Intelligence System")
st.markdown("## 🚀 AI-Powered Civic Intelligence System")
st.markdown("---")

# Complaint display
st.write("### 📌 Complaint:")
st.write(state.text)

# AI Suggestion
ai_action = simple_ai_predict(state.text)
st.write(f"🤖 AI Suggestion: **{ai_action}**")

# Department Suggestion
dept = get_department(state.text)
st.write(f"🏢 Suggested Department: {dept}")

# User input
action = st.selectbox("Select Priority", env.actions)

# ---------------- SUBMIT ----------------
if st.button("Submit") and not st.session_state.done:
    next_state, reward, done, info = env.step(Action(priority=action))

    # Update metrics
    st.session_state.score += reward.value
    st.session_state.total_count += 1

    if action == info["correct"]:
        st.session_state.correct_count += 1

    # Accuracy
    accuracy = (
        st.session_state.correct_count / st.session_state.total_count
        if st.session_state.total_count > 0 else 0
    )

    # Results
    st.success(f"✅ Correct: {info['correct']}")
    st.info(f"🎯 Reward: {reward.value}")
    st.write(f"🏆 Total Score: {st.session_state.score}")
    st.write(f"📊 Accuracy: {accuracy*100:.2f}%")

    # Progress
    progress = st.session_state.total_count / len(env.data)
    st.progress(progress)

    # Next state
    if not done:
        st.session_state.state = next_state
    else:
        st.session_state.done = True
        st.warning("🎉 All complaints processed!")

# ---------------- RESET ----------------
if st.button("🔄 Restart"):
    st.session_state.env = ComplaintEnv(difficulty)
    st.session_state.state = st.session_state.env.reset()
    st.session_state.score = 0
    st.session_state.done = False
    st.session_state.correct_count = 0
    st.session_state.total_count = 0