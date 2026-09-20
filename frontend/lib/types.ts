export type Citation = { clause_id: string; section_ref: string; page: number; quote: string };
export type Extraction = { field_name: string; value: string; confidence: number; citation: Citation; review_status: string };
export type Risk = { id: string; category: string; severity: "high" | "medium" | "low"; explanation: string; recommendation: string; citation: Citation; status: string };
export type Obligation = { id: string; description: string; obligation_type: string; responsible_party: string; due_rule?: string; due_date?: string; owner?: string; status: string; citation: Citation };
export type Clause = { id: string; section_ref: string; heading: string; text: string; clause_type: string; page_start: number };
export type Contract = { id: string; title: string; contract_type: string; processing_status: string; summary: string; raw_text: string; clauses: Clause[]; extractions: Extraction[]; risks: Risk[]; obligations: Obligation[] };
