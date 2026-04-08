---
title: Naarad OpenEnv
emoji: 🧠
colorFrom: blue
colorTo: green
sdk: docker
---

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square)
![OpenEnv](https://img.shields.io/badge/OpenEnv-Compliant-green?style=flat-square)
![AI](https://img.shields.io/badge/AI-LLM%20+%20Rule--Based-orange?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production--Ready-success?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

# 🧠 Naarad OpenEnv  
### AI-Powered Complaint Prioritization Environment for Real-World Governance

> 🚀 A real-world AI environment where agents learn to prioritize and route citizen complaints using structured rewards and multi-task evaluation.

---

## 🌍 Problem Statement

Public grievance systems handle thousands of complaints daily but lack intelligent prioritization, causing delays in critical issue resolution.

---

## 💡 Solution

A reinforcement learning environment where agents learn to:

- 📌 Prioritize complaints  
- 🏢 Route them effectively  
- ⚡ Optimize decisions using reward-based feedback  

---

## ⚙️ Environment Description

This environment simulates a **complaint triage system**:

1. Agent receives a complaint  
2. Agent selects a priority level  
3. Environment evaluates the action  
4. Returns reward + next complaint  

💡 The environment incorporates **context-aware grading** and penalizes **underestimation of critical issues**, reflecting real-world risk-sensitive decision-making.

---

## 📥 Observation Space

```python
Observation(text: str)
```
---
## 🎯 Action Space

["low", "medium", "high", "critical"]

---

## Reward Function

✅ Exact match → 1.0
⚠️ Close prediction → 0.7
❌ Moderate error → 0.3
🚫 Severe mismatch → 0.0
🔻 Underestimating critical issues → additional penalty

---

## 🔁 Episode Flow
  reset() → returns first complaint
  step(action) → returns next complaint + reward
  The episode ends after all complaints are processed

---

## 📂 Project Structure

  env/        # Environment logic
  agent/      # Rule-based & baseline agents
  tasks/      # Dataset (easy, medium, hard)
  app/        # Streamlit UI
  config/     # OpenEnv config
  scripts/    # Execution scripts

---

## ⚙️ Setup Instructions
  git clone https://github.com/saket-pathak/naarad-openenv.git
  cd naarad-openenv

  python -m venv .venv
  .venv\Scripts\activate

  pip install -r requirements.txt
  
---

## ▶️ Run Locally
  streamlit run app/app.py

---

## 🐳 Docker Support

  docker build -t naarad-env .
  docker run -p 7860:7860 naarad-env

---

## 📜 License

  MIT License


