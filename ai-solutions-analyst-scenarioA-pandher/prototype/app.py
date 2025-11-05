# prototype/app.py
import os
from fastapi import FastAPI
from pydantic import BaseModel
from .router import rule_based_classify, llm_refine

app = FastAPI(title="Scenario A Triage Prototype")

class TriageRequest(BaseModel):
    subject: str
    body: str
    source: str  # email | form | phone

@app.post("/triage")
def triage(req: TriageRequest):
    pred = rule_based_classify(req.subject, req.body)
    pred = llm_refine(pred, req.subject, req.body)

    # Attach minimal audit fields for ops demo
    return {
        "input": req.dict(),
        "decision": pred,
        "audit": {
            "version": "v0.1",
            "auto_action_policy": "auto if confidence >= ROUTING_CONFIDENCE_THRESHOLD and category != 'uncertain'",
            "threshold": float(os.getenv("ROUTING_CONFIDENCE_THRESHOLD", "0.80"))
        }
    }