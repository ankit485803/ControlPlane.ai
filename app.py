import streamlit as st
import json
from core.engine import ControlPlaneEngine
from core.policies import POLICIES
import json

# Load sample scenarios from JSON
with open("data/sample_scenarios.json", "r") as f:
    data = json.load(f)
    sample_scenarios = {item["title"]: item for item in data["scenarios"]}

selected_sample_title = st.sidebar.selectbox("Load Pre-Configured Test Scenario:", list(sample_scenarios.keys()))
default_data = sample_scenarios[selected_sample_title]



st.set_page_config(page_title="ControlPlane.ai | AI Observability & Governance Layer", layout="wide")

st.title("🛡️ ControlPlane.ai")
st.subheader("Real-Time AI Observability, Governance & Cost Mitigation Engine")

engine = ControlPlaneEngine()

# Sidebar: Configuration
st.sidebar.header("Enterprise Context & Policy")
use_case = st.sidebar.selectbox(
    "Select AI Use Case Track:",
    options=list(POLICIES.keys()),
    format_func=lambda k: POLICIES[k]["name"]
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Latency Budget:** `{POLICIES[use_case]['latency_budget_ms']} ms`")
st.sidebar.markdown(f"**PII Enforcement:** `{POLICIES[use_case]['pii_action']}`")
st.sidebar.markdown(f"**Hallucination Threshold:** `{POLICIES[use_case]['hallucination_threshold']}`")

# Sample Scenarios
sample_scenarios = {
    "1. PII Leakage Scenario": {
        "prompt": "Get customer account details for user ID 4081",
        "response": "User Harsh Kumar's registered email is harsh@example.com and Aadhaar is 5412-8890-1234.",
        "context": "User ID 4081: Registered under Harsh Kumar, active tier."
    },
    "2. Hallucination / Contradiction Scenario": {
        "prompt": "What is the battery warranty on the 2026 EV model?",
        "response": "The 2026 EV model includes a lifetime unlimited battery replacement guarantee.",
        "context": "Warranty terms: 2026 EV battery pack is covered for 8 years or 100,000 miles, whichever comes first."
    },
    "3. Semantic Cache Hit (Cost Optimization)": {
        "prompt": "What is the company refund policy?",
        "response": "Our policy allows full refunds within 30 days of purchase.",
        "context": "Corporate policy doc #12"
    },
    "4. Clean Pass Scenario": {
        "prompt": "Summarize the Q3 server uptime.",
        "response": "Server uptime for Q3 was maintained at 99.98% across all primary regions.",
        "context": "Q3 Infrastructure summary: Regional server availability averaged 99.98%."
    }
}

selected_sample = st.selectbox("Load Pre-Configured Test Scenario:", list(sample_scenarios.keys()))
default_data = sample_scenarios[selected_sample]

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📥 Ingress & LLM Interaction")
    prompt_input = st.text_area("User / Agent Prompt:", value=default_data["prompt"], height=70)
    context_input = st.text_area("Reference Enterprise Context (RAG):", value=default_data["context"], height=90)
    raw_response = st.text_area("Raw LLM Output (Unscreened):", value=default_data["response"], height=120)
    run_btn = st.button("🚀 Process Through ControlPlane.ai", type="primary")

with col2:
    st.markdown("### 📤 Governed Output & Real-Time Telemetry")
    if run_btn:
        result = engine.process(use_case, prompt_input, raw_response, context_input)
        
        # Status Banner
        action = result["action"]
        if "BLOCK" in action:
            st.error(f"🛑 Decision: **{action}**")
        elif "EDIT" in action:
            st.warning(f"✏️ Decision: **{action}**")
        elif "ESCALATE" in action:
            st.warning(f"⚠️ Decision: **{action}**")
        else:
            st.success(f"✅ Decision: **{action}**")

        st.markdown("**Delivered Output to User:**")
        st.info(result["final_response"])

        st.markdown("#### ⏱️ Latency & Execution Breakdown")
        m1, m2, m3 = st.columns(3)
        m1.metric("Engine Latency", f"{result['latency_ms']} ms", delta=f"{result['latency_budget_ms'] - result['latency_ms']} ms budget left")
        
        if "cost_metrics" in result:
            m2.metric("Tokens Processed", result["cost_metrics"]["total_tokens"])
            m3.metric("Est. Inference Cost", f"${result['cost_metrics']['estimated_cost_usd']}")
        elif "cost_saved_usd" in result:
            m2.metric("Tokens Processed", "0 (Cache)")
            m3.metric("Cost Saved", f"${result['cost_saved_usd']}")

        st.markdown("#### 📋 Inspection Details")
        for r in result["reasons"]:
            st.write(f"- {r}")