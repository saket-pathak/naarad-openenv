---
title: Naarad OpenEnv
emoji: 🧠
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: "0.0.0"
python_version: "3.10"
app_file: main.py
pinned: false
---

# 🧠 Naarad OpenEnv

### AI-Powered Complaint Prioritization System (OpenEnv Compatible)

> 🚀 A real-world AI environment where agents learn to intelligently prioritize and route citizen complaints using structured rewards and contextual reasoning.

---

## 🌍 Problem Statement

Public grievance systems handle thousands of complaints daily but lack intelligent prioritization, leading to:

- Delayed response to critical issues 🚨
- Inefficient resource allocation ⚙️
- Poor citizen satisfaction 😞

---

## 💡 Solution

Naarad OpenEnv provides a **reinforcement learning environment** where AI agents learn to:

- 📌 Prioritize complaints based on severity
- 🏢 Route issues to appropriate departments
- ⚡ Optimize decisions using reward-based feedback

---

## ⚙️ How It Works

1. Agent receives a complaint (text input)
2. Agent selects a priority level
3. Environment evaluates the decision
4. Returns:
   - reward 🎯
   - next complaint 🔁

---

## 📥 Observation Space

```python
Observation(text: str)
```

## 🎯 Action Space

```python
["low", "medium", "high", "critical"]
```

---

## 🏆 Reward System

| Scenario | Reward |
|---|---|
| ✅ Exact match | 1.0 |
| ⚠️ Close prediction | 0.7 |
| ❌ Moderate error | 0.3 |
| 🚫 Severe mismatch | 0.0 |
| 🔻 Underestimating critical | Extra penalty |

---

## 🔁 Episode Flow

```
POST /reset  → returns first complaint
POST /step   → returns next complaint + reward
```

Episode ends after all complaints are processed.

---

## 🚀 API Endpoints

### 🔹 Reset Environment

```
POST /reset
```

### 🔹 Take Action

```
POST /step
Content-Type: application/json

{
  "priority": "high"
}
```

---

## 🧪 Try It Live

👉 **API Docs (Swagger UI):** https://saketpathak-naarad-openenv-final.hf.space/docs  
👉 **Base URL:** https://saketpathak-naarad-openenv-final.hf.space

---

## 📂 Project Structure

```
env/              # Environment logic
agent/            # Rule-based & baseline agents
tasks/            # Dataset (easy, medium, hard)
main.py           # FastAPI backend (API endpoints)
openenv.yaml      # OpenEnv configuration
inference.py      # Evaluation script
Dockerfile        # Deployment setup
requirements.txt
```

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/saket-pathak/naarad-openenv.git
cd naarad-openenv

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
```

---

## ▶️ Run Locally

```bash
uvicorn main:app --reload
```

---

## 🐳 Docker Deployment

```bash
docker build -t naarad-env .
docker run -p 7860:7860 naarad-env
```

---

## 🤖 Inference (Evaluation)

```bash
python inference.py
```

---

## 🎯 Key Highlights

- ✅ OpenEnv compliant
- 🤖 Supports AI agents (rule-based + ML-ready)
- ⚡ Real-world inspired reward system
- 🌐 Fully deployed via FastAPI + Docker
- 🧪 Ready for automated evaluation

---

## 📜 License

MIT License

---

## 🔗 References

OpenEnv Docs: https://huggingface.co/docs/hub/spaces-config-reference
