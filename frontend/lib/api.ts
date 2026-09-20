import type { Contract, Obligation } from "./types";

const base = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";
async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${base}${path}`, options);
  if (!response.ok) throw new Error((await response.json().catch(() => null))?.detail ?? "Request failed");
  return response.json() as Promise<T>;
}
export const api = {
  list: () => request<Contract[]>("/api/contracts", { cache: "no-store" }),
  demo: () => request<Contract>("/api/contracts/demo", { method: "POST" }),
  upload: (file: File) => { const body = new FormData(); body.append("file", file); return request<Contract>("/api/contracts/upload", { method: "POST", body }); },
  ask: (id: string, question: string) => request<{ answer: string; citations: { section_ref: string }[]; confidence: number }>(`/api/contracts/${id}/ask`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question }) }),
  updateObligation: (contractId: string, obligationId: string, status: string) => request<Obligation>(`/api/contracts/${contractId}/obligations/${obligationId}`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ status }) })
};
