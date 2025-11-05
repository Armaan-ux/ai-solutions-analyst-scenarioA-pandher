# prototype/router.py
import os
from typing import Dict, Any

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CONF_THRESHOLD = float(os.getenv("ROUTING_CONFIDENCE_THRESHOLD", "0.80"))

# Very lightweight keyword heuristics to classify request category + language.
def rule_based_classify(subject: str, body: str) -> Dict[str, Any]:
    text = f"{subject} {body}".lower()

    # language
    es_markers = ["por favor", "no puede", "urgente", "gracias", "gerente"]
    language = "ES" if any(tok in text for tok in es_markers) else "EN"

    # category
    if any(k in text for k in ["sick", "no puede trabajar", "sick call", "illness"]):
        category = "sick_call"
    elif any(k in text for k in ["ticket", "update ticket", "case update"]):
        category = "ticket_update"
    elif any(k in text for k in ["vendor", "invoice", "supplier"]):
        category = "vendor_issue"
    elif any(k in text for k in ["follow up", "overdue", "client follow"]):
        category = "client_followup"
    else:
        category = "uncertain"

    # route
    routing = {
        "sick_call": "HR_Team",
        "ticket_update": "FieldOps",
        "vendor_issue": "Vendor_Team",
        "client_followup": "Client_Success",
        "uncertain": "Manual_Review"
    }[category]

    # naive confidence
    confidence = 0.92 if category != "uncertain" else 0.50

    return {
        "language": language,
        "category": category,
        "route_to": routing,
        "confidence": confidence,
        "auto_action": confidence >= CONF_THRESHOLD and category != "uncertain"
    }

# Optional: placeholder for LLM-assisted refinement (kept off if no API key)
def llm_refine(pred: Dict[str, Any], subject: str, body: str) -> Dict[str, Any]:
    # For the assessment, we keep this a stub so the prototype runs offline.
    # In a real env, you would call OpenAI with a system prompt that enforces:
    # - output schema
    # - bilingual handling
    # - explanation/rationale
    # If OPENAI_API_KEY is not set, return pred untouched.
    if not OPENAI_API_KEY:
        return pred
    # Example: attach rationale field to show we *would* add it
    pred = dict(pred)
    pred["rationale"] = "LLM-assisted classification rationale would appear here."
    return pred