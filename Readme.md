![Python](https://img.shields.io/badge/Python-3.10-blue)
![Framework](https://img.shields.io/badge/Framework-OpenEnv-green)
![UI](https://img.shields.io/badge/UI-Streamlit-red)
![License](https://img.shields.io/badge/License-MIT-yellow)



# 🧠 Naarad OpenEnv  
### AI-Powered Complaint Prioritization Environment for Real-World Governance

---

## 🚀 Problem Statement

Public grievance systems in many regions (like municipal portals, helplines, etc.) handle **thousands of complaints daily**, ranging from minor civic issues to critical emergencies.

However:
- Complaints are often processed manually
- Urgent cases may get delayed
- No intelligent prioritization or routing exists

👉 This leads to **inefficient governance and slow response times**

---

## 💡 Our Solution

**Naarad OpenEnv** is a **real-world AI training environment** where agents learn to:

- 📌 Prioritize citizen complaints (low → critical)
- 🏢 Route them to correct departments
- ⚡ Optimize decision-making using reward-based learning

---

## 🧠 Why This Matters

This is NOT a toy problem.

It directly simulates:
- Customer support triage  
- Government grievance systems  
- Emergency response prioritization  

👉 A step toward **AI-assisted governance systems**

---

## ⚙️ OpenEnv Environment Design

We fully implement the **OpenEnv specification**:

### 🔹 Core Interface

- `reset()` → returns initial Observation  
- `step(action)` → returns `(observation, reward, done, info)`  
- `state()` → returns current Observation  

---

### 🔹 Typed Models (Pydantic)

```python
Observation(text: str)
Action(priority: str)
Reward(value: float)
