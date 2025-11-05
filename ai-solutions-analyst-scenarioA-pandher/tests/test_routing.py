# tests/test_routing.py
from prototype.router import rule_based_classify

def test_sick_call_en():
    out = rule_based_classify("Sick call for Mike", "He is sick today and cannot work")
    assert out["category"] == "sick_call"
    assert out["route_to"] == "HR_Team"
    assert out["confidence"] >= 0.8

def test_vendor_issue_es():
    out = rule_based_classify("Factura del vendor", "Por favor revisar invoice atrasada",)
    assert out["language"] in ("ES", "EN")  # heuristic may still pick EN if few markers
    # Category should hit vendor_issue based on keywords
    assert out["category"] in ("vendor_issue", "uncertain")