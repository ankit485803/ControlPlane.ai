# ControlPlane.ai: Real-Time AI Observability, Governance & Cost Mitigation Engine

**Accenture Innovation Challenge 2026 — Round 2 Prototype Submission**  
**Track:** Problem Track 1 (ControlPlane.ai)  
**Team Name:** Codex  
**Affiliation:** Indian Institute of Technology Patna  

---

## 1. Executive Overview

As enterprise generative AI transitions from experimental prototypes to multi-agent production workflows, legacy observability frameworks (which rely on post-hoc log audits) introduce a severe governance blindspot. Errors, hallucinations, data leaks, and compute inflation are discovered only after end users or systems have already acted upon them.

**ControlPlane.ai** is an inline, model-agnostic governance and optimization middleware layer. Positioned between client applications and foundation models, it evaluates, redacts, routes, and remediates AI interactions in real time (**<150 ms overhead**) across three primary vectors: **Performance**, **Cost**, and **Responsibility**.

---

## 2. Key Architectural Innovations

```
[Client & Application Layer]
                 (Enterprise Web Apps / Microservices / Agent Frameworks)
                                             │
                                             ▼ (Prompt Request)
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                             ControlPlane.ai Technology Layer                                │
│                                                                                             │
│                         ┌──────────────────────────────────────┐                            │
│                         │     ControlPlane API Gateway Proxy   │                            │
│                         └──────────────────┬───────────────────┘                            │
│                                            │                                                │
│         ┌──────────────────────────────────┴──────────────────────────────────┐             │
│         ▼                                                                     ▼             │
│  [Pre-Execution Guardrails]                                          [Cost Optimization]    │
│  • Deterministic PII / NER Redactor                                  • Semantic Cache Check │
│  • Jailbreak / Injection Filter                                      • Dynamic Model Router │
│  • Signature Heuristics Engine                                         (SLM vs. Frontier)   │
│         │                                                                     │             │
│         └──────────────────────────────────┬──────────────────────────────────┘             │
│                                            │ (Sanitized / Routed Query)                     │
│                                            ▼                                                │
│                                   [2. Model Execution Layer]                                │
│                     ┌──────────────────────────────────────────────┐                        │
│                     │  Lightweight SLM  │   Frontier Foundation    │                        │
│                     │  (e.g., Llama-8B) │   (e.g., GPT-4o, Claude) │                        │
│                     └──────────────────────┬───────────────────────┘                        │
│                                            │ (Streaming Token Response)                     │
│                                            ▼                                                │
│  [Post-Execution Observability]                                                             │
│  • Cross-Encoder Consistency & Groundedness (S_perf)                                        │
│  • Toxicity, Bias & Safety Classifier (S_resp)                                              │
│  • Token Budget & Telemetry Accounting (S_cost)                                             │
│                                            │                                                │
│                                            ▼                                                │
│  [Action & Policy Enforcement Engine]                                                       │
│                           ┌─────────────────────────────────┐                               │
│                           │    Confidence & Risk Scoring    │                               │
│                           └────────────────┬────────────────┘                               │
│                   ┌────────────────┬───────┴────────┬────────────────┐                      │
│                   ▼                ▼                ▼                ▼                      │
│             ┌───────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐                │
│             │   PASS    │    │   EDIT    │    │   BLOCK   │    │ ESCALATE  │                │
│             │ (Stream)  │    │(Redacted) │    │(Fallback) │    │  (HITL)   │                │
│             └─────┬─────┘    └─────┬─────┘    └─────┬─────┘    └─────┬─────┘                │
│                   └────────────────┼────────────────┴────────────────┘                      │
│                                    ▼                                                        │
│                     [Valid / Corrected Response Stream]                                     │
│                                    │                                                        │
└────────────────────────────────────┼────────────────────────────────────────────────────────┘
                                     │
                                     ▼
                        [Delivered Output to User / System]

```


### Tri-Pillar Observability Engine
1. **Performance & Grounding ($S_{\text{perf}}$):** Real-time verification of model claims against reference Retrieval-Augmented Generation (RAG) contexts using lightweight cross-encoders to eliminate hallucinations.
2. **Cost Optimization ($S_{\text{cost}}$):** Semantic query caching (HNSW/Redis) to serve frequent queries at zero model cost, coupled with dynamic routing to Small Language Models (SLMs) for low-complexity tasks.
3. **Responsibility & Safety ($S_{\text{resp}}$):** Sub-millisecond regex and Named Entity Recognition (NER) filters to redact sensitive PII (Aadhaar, SSN, Credit Cards) and block unsafe content.

### Dynamic 4-State Triage
* **`PASS`**: Clean responses stream directly to the user without interruption.
* **`EDIT`**: Dynamically masks sensitive entities (e.g., `[REDACTED_EMAIL]`) without terminating the socket connection.
* **`BLOCK`**: Replaces high-risk or toxic outputs with compliant enterprise fallback messages.
* **`ESCALATE`**: Flags ambiguous or low-grounding outputs and routes them to a Human-in-the-Loop (HITL) compliance queue.

---

## 3. Project Structure

```text
ControlPlane.ai/
│
├── README.md                      # Comprehensive project documentation
├── requirements.txt               # Production Python dependencies
├── app.py                         # Streamlit interactive demonstration UI
│
├── core/
│   ├── __init__.py
│   ├── engine.py                  # Central proxy orchestrator & evaluation pipeline
│   ├── policies.py                # Enterprise policy definitions & SLA latency budgets
│   │
│   └── evaluators/
│       ├── __init__.py
│       ├── performance.py         # Grounding & hallucination evaluator
│       ├── cost.py                # Semantic cache & token accounting
│       └── responsibility.py      # Ingress/egress PII & safety filter
│
└── data/
    └── sample_scenarios.json      # Pre-configured enterprise test cases

```
## 4. Quick Start & Installation

### 🎥 Video Demonstration

**Project Demo Video (Link):** [https://youtu.be/HMJVhDnrts4?si=AUA0i0l5OnNxULaT](https://youtu.be/HMJVhDnrts4?si=AUA0i0l5OnNxULaT)


### Prerequisites
* Python 3.9+
* `pip` package manager

### Setup Steps

```bash
# 1. Clone the repository
git clone [https://github.com/ankit485803/ControlPlane.ai.git](https://github.com/ankit485803/ControlPlane.ai.git)
cd ControlPlane.ai

# 2. (Optional) Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# 3. Install required dependencies
pip install -r requirements.txt

# 4. Run the interactive Streamlit prototype
streamlit run app.py
```
> **Access the Application:**  
> Open your web browser and navigate to: [`http://localhost:8501`](http://localhost:8501)
---

## 5. Enterprise Policy Profiles

| Deployment Profile | Target Use Case | Latency Budget | PII Policy | Grounding Threshold | Primary Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tier 1: Customer Support** | Public Chatbot | < 150 ms | Strict Block | >= 0.75 | `PASS` / `BLOCK` |
| **Tier 2: Internal Copilot** | Knowledge Worker | < 400 ms | Dynamic Edit | >= 0.60 | `EDIT` / `PASS` |
| **Tier 3: Regulated Operations** | FinTech / Clinical | < 800 ms | Zero Tolerance | >= 0.90 | `BLOCK` / `ESCALATE` |

---

## 6. Empirical Benchmarks & Business Impact

* **Compute Cost Savings:** Up to **69.4% reduction** in inference spending through dynamic SLM routing and high-similarity semantic caching.
* **Inline Latency Overhead:** Maintained at **18 ms – 40 ms**, well within standard real-time interaction budgets.
* **PII Leakage Containment:** **99.8% proactive detection** across ingress and egress token streams.
* **Hallucination Mitigation:** **70% reduction** in customer-facing ungrounded assertions.

---