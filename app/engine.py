
import re
from datetime import date, timedelta
from datetime import date, datetime, timedelta
from difflib import SequenceMatcher
    "sla": ("service level", "uptime", "availability"),
    "term": ("effective", "expiration", "expires", "term"),
}

def find_dates(text: str) -> list[str]:
    pattern = r"(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}"
    return re.findall(pattern, text, re.I)


def parse_date(text: str | None) -> date | None:
    """Parse only the explicit date format emitted by ``find_date``."""
    if not text:
        return None
    try:
        return datetime.strptime(text, "%B %d, %Y").date()
    except ValueError:
        return None


def extract(contract: Contract) -> list[Extraction]:
    results: list[Extraction] = []
    all_text = contract.raw_text
    fields = [("effective_date", "effective date", "term"), ("expiration_date", "expiration", "term"), ("renewal_terms", "renewal", "renewal"), ("payment_terms", "payment", "payment"), ("termination_conditions", "termination", "termination")]
            continue
        value = find_date(clause.text) if "date" in field else re.sub(r"\s+", " ", clause.text)[:180]
        if field == "effective_date":
            value = (find_dates(clause.text) or [None])[0]
        elif field == "expiration_date":
            dates = find_dates(clause.text)
            value = dates[-1] if len(dates) > 1 else None
        else:
            value = re.sub(r"\s+", " ", clause.text)[:180]
        if value:

def renewal_notice_date(text: str, expiration_date: date | None) -> tuple[date | None, str | None]:
    """Resolve a notice deadline only when both the period and expiry are explicit."""
    match = re.search(r"(?:at least\s+)?(\d+)\s+days?\s+before", text, re.I)
    if not match or not expiration_date:
        return None, None
    days = int(match.group(1))
    return expiration_date - timedelta(days=days), f"{days} days before expiration date"


def risks(contract: Contract) -> list[RiskFlag]:
    items: list[Obligation] = []
    effective = next((find_date(e.value) for e in contract.extractions if e.field_name == "effective_date"), None)
    effective_date = None
    if effective:
        try: effective_date = date.fromisoformat(__import__('datetime').datetime.strptime(effective, "%B %d, %Y").date().isoformat())
        except ValueError: pass
    effective_date = parse_date(next((e.value for e in contract.extractions if e.field_name == "effective_date"), None))
    expiration_date = parse_date(next((e.value for e in contract.extractions if e.field_name == "expiration_date"), None))
    for clause in contract.clauses:
        if "notice" in lower and "renew" in lower:
            due_date, due_rule = renewal_notice_date(clause.text, expiration_date)
            items.append(Obligation(description="Send non-renewal notice before the renewal deadline", obligation_type="renewal_notice", responsible_party="Contract owner", due_rule="See renewal clause", citation=citation(clause)))
            items.append(Obligation(description="Send non-renewal notice before the renewal deadline", obligation_type="renewal_notice", responsible_party="Contract owner", due_rule=due_rule or "Deadline could not be resolved; review renewal clause", due_date=due_date, citation=citation(clause)))
        if "shall" in lower and clause.clause_type in {"sla", "confidentiality"}:
def analyze(contract: Contract) -> Contract:
    try:
        contract.processing_status = "processing"
        contract.clauses = segment(contract.raw_text)
        if not contract.clauses:
    contract.clauses = segment(contract.raw_text)
    contract.extractions = extract(contract)
    contract.risks = risks(contract)
    contract.obligations = obligations(contract)
    contract.summary = summarize(contract)
            raise ValueError("No clauses could be segmented from the supplied text.")
        contract.extractions = extract(contract)
        contract.risks = risks(contract)
        contract.obligations = obligations(contract)
        contract.summary = summarize(contract)
        contract.processing_status = "ready"
        contract.processing_error = None
    except Exception as exc:
        contract.processing_status = "failed"
        contract.processing_error = "Analysis could not be completed. Review the document text and retry."
        raise ValueError(contract.processing_error) from exc
    return contract
            changes.append({"type": "modified", "section": new_clause.section_ref, "impact": "Clause wording changed; assess business impact.", "citation": citation(new_clause)})
    new_sections = {clause.section_ref for clause in newer.clauses}
    for old_clause in base.clauses:
        if old_clause.section_ref not in new_sections:
            changes.append({"type": "removed", "section": old_clause.section_ref, "impact": "Clause was removed; assess the protection or obligation that changed.", "citation": citation(old_clause)})
    return changes
