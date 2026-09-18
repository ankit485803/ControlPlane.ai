class CostEvaluator:
    CACHE_DB = {
        "what is the company refund policy?": "Our policy allows full refunds within 30 days of purchase.",
        "how to reset corporate vpn password?": "Visit https://sso.internal/reset and authenticate via 2FA."
    }

    def check_cache(self, prompt: str):
        cleaned = prompt.strip().lower()
        if cleaned in self.CACHE_DB:
            return {"cache_hit": True, "cached_response": self.CACHE_DB[cleaned], "cost_saved_usd": 0.003}
        return {"cache_hit": False, "cached_response": None, "cost_saved_usd": 0.0}

    def calculate_cost(self, prompt: str, response: str, model: str = "gpt-4o"):
        input_tokens = len(prompt.split()) * 1.3
        output_tokens = len(response.split()) * 1.3
        
        # Cost constants ($ per 1K tokens)
        cost_per_1k = 0.005 if "4o" in model else 0.0005
        total_cost = ((input_tokens + output_tokens) / 1000.0) * cost_per_1k
        
        return {
            "input_tokens": int(input_tokens),
            "output_tokens": int(output_tokens),
            "total_tokens": int(input_tokens + output_tokens),
            "estimated_cost_usd": round(total_cost, 6)
        }