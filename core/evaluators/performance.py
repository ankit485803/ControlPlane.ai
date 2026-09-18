class PerformanceEvaluator:
    """
    Evaluates factual consistency/hallucination risk between reference context and response.
    """
    def evaluate(self, response: str, reference_context: str = ""):
        if not reference_context:
            return {
                "hallucination_score": 0.1,
                "grounded": True,
                "reason": "General conversational query (No reference context required)"
            }
        
        # Token overlap heuristic (can be swapped with ONNX / NLI cross-encoder)
        ref_words = set(re_tokenize(reference_context.lower()))
        res_words = set(re_tokenize(response.lower()))
        
        # Check factual entity overlap
        missing_entities = [w for w in res_words if len(w) > 5 and w not in ref_words]
        overlap_ratio = len(res_words.intersection(ref_words)) / max(len(res_words), 1)

        hallucination_score = max(0.0, min(1.0, 1.0 - overlap_ratio))
        
        return {
            "hallucination_score": round(hallucination_score, 2),
            "grounded": hallucination_score < 0.45,
            "unsupported_tokens": missing_entities[:3]
        }

def re_tokenize(text):
    import re
    return re.findall(r'\b\w+\b', text)