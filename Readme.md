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
- Prioritize complaints  
- Route them effectively  
- Optimize decisions using rewards  

---

## ⚙️ Environment Description

This environment simulates a **complaint triage system**:

1. Agent receives a complaint  
2. Agent selects a priority  
3. Environment returns reward + next complaint  

---

## 📥 Observation Space

```python
Observation(text: str)

---

## 🎯 Action Space

```text
["low", "medium", "high", "critical"]

---

## 🎯 Reward Function

- ✅ Correct prediction → **1.0**  
- ⚠️ Close prediction → **0.5**  
- ❌ Incorrect prediction → **0.0**  
- 🔻 Large mismatch → penalty applied  

---

## 🔁 Episode Flow

- `reset()` → returns first complaint  
- `step(action)` → returns next complaint  
- Episode ends after all complaints are processed  

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/saket-pathak/naarad-openenv.git
cd naarad-openenv

python -m venv .venv
.venv\Scripts\Activate

pip install -r requirements.txt

## 🐳 Docker Support
docker build -t naarad-env .
docker run naarad-env
