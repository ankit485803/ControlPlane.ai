"""
Defines configurable enterprise risk tolerances and latency budgets across use cases.
"""

POLICIES = {
    "customer_support": {
        "name": "Customer Support Bot (High Risk, Low Latency)",
        "latency_budget_ms": 150,
        "pii_action": "BLOCK",
        "hallucination_threshold": 0.40,
        "toxic_action": "BLOCK",
        "cache_enabled": True
    },
    "internal_copilot": {
        "name": "Internal Employee Copilot (Medium Risk, High Latency Budget)",
        "latency_budget_ms": 400,
        "pii_action": "EDIT",
        "hallucination_threshold": 0.65,
        "toxic_action": "FLAG_ESCALATE",
        "cache_enabled": True
    },
    "regulated_decision_support": {
        "name": "Regulated Decision Engine (Zero Tolerance)",
        "latency_budget_ms": 800,
        "pii_action": "BLOCK",
        "hallucination_threshold": 0.20,
        "toxic_action": "BLOCK",
        "cache_enabled": False
    }
}