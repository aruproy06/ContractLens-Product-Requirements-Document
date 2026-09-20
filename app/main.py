
from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, File, HTTPException, UploadFile
from .engine import analyze, answer, compare
from .models import Contract
from .models import AuditEvent, Contract, ObligationStatus, ReviewStatus


class Question(BaseModel): question: str
class UpdateStatus(BaseModel): status: str; owner: str | None = None
class CompareRequest(BaseModel): base_id: str; new_id: str
class Question(BaseModel):
    question: str

class UpdateStatus(BaseModel):
    status: ObligationStatus
    owner: str | None = None

class ReviewDecision(BaseModel):
    status: ReviewStatus
    note: str | None = None

class RiskDecision(BaseModel):
    status: str
    note: str | None = None

class CompareRequest(BaseModel):
    base_id: str
    new_id: str



def record(contract: Contract, entity_type: str, entity_id: str, action: str, before: dict | None = None, after: dict | None = None) -> None:
    contract.audit_log.append(AuditEvent(entity_type=entity_type, entity_id=entity_id, action=action, before=before, after=after))

@app.get("/")

@app.get("/api/health")
def health():
    return {"status": "ok", "contracts_in_memory": len(STORE)}

@app.get("/api/dashboard")
def dashboard():
    contracts = list(STORE.values())
    obligations = [item for contract in contracts for item in contract.obligations]
    risks = [item for contract in contracts for item in contract.risks]
    return {
        "active_contracts": len([item for item in contracts if item.processing_status == "ready"]),
        "upcoming_obligations": len([item for item in obligations if item.status in {"open", "in_progress"}]),
        "open_high_risks": len([item for item in risks if item.severity == "high" and item.status == "open"]),
        "needs_review": len([item for item in risks if item.status == "open"]),
    }

@app.post("/api/contracts/demo")
def demo():
    contract = analyze(Contract(title="Acme MSA 2026", raw_text=DEMO, processing_status="ready"))
    contract = analyze(Contract(title="Acme MSA 2026", raw_text=DEMO))
    record(contract, "contract", contract.id, "analyzed")
    STORE[contract.id] = contract
    if not text.strip(): raise HTTPException(400, "No text could be extracted. OCR is not enabled in this MVP.")
    contract = analyze(Contract(title=Path(file.filename).stem, raw_text=text, processing_status="ready"))
    title = Path(file.filename).stem.strip()[:180] or "Untitled contract"
    try:
        contract = analyze(Contract(title=title, raw_text=text))
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    record(contract, "contract", contract.id, "uploaded_and_analyzed")
    STORE[contract.id] = contract
def update_obligation(contract_id: str, obligation_id: str, payload: UpdateStatus):
    current = get_contract(contract_id)
    item = next((o for o in get_contract(contract_id).obligations if o.id == obligation_id), None)
    item = next((o for o in current.obligations if o.id == obligation_id), None)
    if not item: raise HTTPException(404, "Obligation not found")
    before = item.model_dump(mode="json")
    item.status, item.owner = payload.status, payload.owner or item.owner
    record(current, "obligation", item.id, "updated", before, item.model_dump(mode="json"))
    return item

@app.patch("/api/contracts/{contract_id}/extractions/{field_name}")
def review_extraction(contract_id: str, field_name: str, payload: ReviewDecision):
    current = get_contract(contract_id)
    item = next((value for value in current.extractions if value.field_name == field_name), None)
    if not item:
        raise HTTPException(404, "Extraction not found")
    before = item.model_dump(mode="json")
    item.review_status = payload.status
    record(current, "extraction", field_name, f"review_{payload.status.value}", before, item.model_dump(mode="json"))
    return item

@app.patch("/api/contracts/{contract_id}/risks/{risk_id}")
def review_risk(contract_id: str, risk_id: str, payload: RiskDecision):
    allowed = {"open", "confirmed", "dismissed", "escalated"}
    if payload.status not in allowed:
        raise HTTPException(422, f"Status must be one of: {', '.join(sorted(allowed))}")
    current = get_contract(contract_id)
    item = next((value for value in current.risks if value.id == risk_id), None)
    if not item:
        raise HTTPException(404, "Risk flag not found")
    before = item.model_dump(mode="json")
    item.status = payload.status
    record(current, "risk_flag", item.id, f"review_{payload.status}", before, item.model_dump(mode="json"))
    return item

@app.get("/api/contracts/{contract_id}/audit-log")
def audit_log(contract_id: str):
    return get_contract(contract_id).audit_log

@app.post("/api/compare")
