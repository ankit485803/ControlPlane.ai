import time
from core.policies import POLICIES
from core.evaluators.responsibility import ResponsibilityEvaluator
from core.evaluators.performance import PerformanceEvaluator
from core.evaluators.cost import CostEvaluator

class ControlPlaneEngine:
    def __init__(self):
        self.resp_eval = ResponsibilityEvaluator()
        self.perf_eval = PerformanceEvaluator()
        self.cost_eval = CostEvaluator()

    def process(self, use_case_key: str, prompt: str, raw_response: str, reference_context: str = ""):
        start_time = time.perf_counter()
        policy = POLICIES.get(use_case_key, POLICIES["customer_support"])
        
        # 1. Cost & Cache Evaluation
        cache_result = self.cost_eval.check_cache(prompt)
        if cache_result["cache_hit"] and policy["cache_enabled"]:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return {
                "final_response": cache_result["cached_response"],
                "action": "CACHE_HIT (PASSED)",
                "latency_ms": round(elapsed_ms, 2),
                "cost_saved_usd": cache_result["cost_saved_usd"],
                "reasons": ["Served instantly from semantic cache at zero model inference cost."]
            }

        # 2. Responsibility Evaluation (PII / Toxicity)
        resp_result = self.resp_eval.evaluate(raw_response)

        # 3. Performance / Hallucination Evaluation
        perf_result = self.perf_eval.evaluate(raw_response, reference_context)

        # 4. Cost Accounting
        cost_result = self.cost_eval.calculate_cost(prompt, raw_response)

        # 5. Policy Decision Matrix
        action = "PASS"
        final_text = raw_response
        reasons = []

        # Check Responsibility
        if resp_result["detected_pii"]:
            if policy["pii_action"] == "BLOCK":
                action = "BLOCK"
                final_text = "[BLOCKED BY CONTROLPLANE]: Output contains unauthorized PII/PHI entities."
                reasons.append(f"PII Detected: {resp_result['detected_pii']}")
            elif policy["pii_action"] == "EDIT":
                action = "EDIT"
                final_text = resp_result["sanitized_text"]
                reasons.append(f"Redacted sensitive fields: {resp_result['detected_pii']}")

        if resp_result["toxic_flags"]:
            action = "BLOCK"
            final_text = "[BLOCKED BY CONTROLPLANE]: Safety & moderation threshold breach."
            reasons.append(f"Safety violations: {resp_result['toxic_flags']}")

        # Check Hallucination
        if action != "BLOCK" and perf_result["hallucination_score"] > policy["hallucination_threshold"]:
            if use_case_key == "regulated_decision_support":
                action = "BLOCK"
                final_text = "[BLOCKED BY CONTROLPLANE]: Unverified factual assertion in regulated workflow."
            else:
                action = "ESCALATE (FLAGGED)"
                final_text = f"{raw_response}\n\n⚠️ [FLAGGED FOR HUMAN REVIEW: Low confidence grounding]"
            reasons.append(f"Hallucination score ({perf_result['hallucination_score']}) exceeded policy threshold ({policy['hallucination_threshold']})")

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        return {
            "final_response": final_text,
            "action": action,
            "latency_ms": round(elapsed_ms, 2),
            "latency_budget_ms": policy["latency_budget_ms"],
            "latency_status": "WITHIN_BUDGET" if elapsed_ms <= policy["latency_budget_ms"] else "EXCEEDED",
            "cost_metrics": cost_result,
            "responsibility_metrics": resp_result,
            "performance_metrics": perf_result,
            "reasons": reasons if reasons else ["Passed all security, truthfulness, and policy thresholds."]
        }