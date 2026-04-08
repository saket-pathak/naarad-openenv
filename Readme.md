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

Public grievance systems (municipal portals, helplines, etc.) handle **thousands of complaints daily**, ranging from minor civic issues to critical emergencies.

However:
- ❌ Complaints are processed manually  
- ❌ Urgent cases are often delayed  
- ❌ No intelligent prioritization or routing exists  

👉 This leads to **inefficient governance and slow response times**

---

## 💡 Our Solution

**Naarad OpenEnv** is a **real-world reinforcement learning environment** where AI agents learn to:

- 📌 Classify complaint priority (**low → critical**)  
- 🏢 Route complaints to appropriate departments  
- ⚡ Optimize decisions through reward-based learning  

---

## 🧠 Why This Matters

This is **not a toy problem**.

It directly applies to:
- Government grievance systems  
- Customer support triage  
- Emergency prioritization workflows  

👉 Enabling **AI-assisted governance systems**

---

## ⚙️ OpenEnv Compliance

This project fully implements the **OpenEnv specification**:

### 🔹 Core Interface

- `reset()` → returns initial **Observation**  
- `step(action)` → returns `(Observation, Reward, done, info)`  
- `state()` → returns current Observation  

---

### 🔹 Typed Models (Pydantic)

```python
Observation(text: str)
Action(priority: str)
Reward(value: float)
