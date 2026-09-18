import re

class ResponsibilityEvaluator:
    # Regex patterns for common sensitive entities
    PATTERNS = {
        "EMAIL": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
        "SSN_AADHAAR": r'\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b|\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        "CREDIT_CARD": r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
        "API_KEY": r'(?i)(?:api[_-]?key|secret|token)[\s:=]+["\']?([a-zA-Z0-9_\-]{16,})["\']?'
    }
    
    TOXIC_KEYWORDS = ["fraud", "bypass security", "exploit", "hack database", "discriminate against"]

    def evaluate(self, text: str):
        detected_entities = []
        sanitized_text = text

        # 1. Detect and Mask PII
        for entity_type, pattern in self.PATTERNS.items():
            matches = list(re.finditer(pattern, sanitized_text))
            if matches:
                detected_entities.append(entity_type)
                sanitized_text = re.sub(pattern, f"[REDACTED_{entity_type}]", sanitized_text)

        # 2. Check Moderation/Safety
        toxic_matches = [word for word in self.TOXIC_KEYWORDS if word in text.lower()]

        score = 0.0
        if detected_entities:
            score += 0.5
        if toxic_matches:
            score += 0.5

        return {
            "score": min(score, 1.0),
            "detected_pii": detected_entities,
            "toxic_flags": toxic_matches,
            "sanitized_text": sanitized_text
        }