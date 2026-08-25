"use client";

import { ArrowDown, ArrowUp, ArrowUpDown } from "lucide-react";
import type { Transaction, TransactionFilters } from "@/lib/types";
import { Badge } from "@/components/ui/Badge";
import { EmptyState } from "@/components/ui/EmptyState";
import { Spinner } from "@/components/ui/Spinner";

const currency = new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", minimumFractionDigits: 2 });
const dateTime = new Intl.DateTimeFormat("en-IN", { day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" });

type Props = { records: Transaction[]; loading: boolean; filters: TransactionFilters; onSort: (sortBy: "timestamp" | "amount") => void; onSelect: (transaction: Transaction) => void };

function SortButton({ label, field, filters, onSort }: { label: string; field: "timestamp" | "amount"; filters: TransactionFilters; onSort: Props["onSort"] }) {
  const active = filters.sort_by === field;
  const Icon = !active ? ArrowUpDown : filters.sort_order === "asc" ? ArrowUp : ArrowDown;
  return <button type="button" onClick={() => onSort(field)} className="inline-flex items-center gap-1 font-semibold text-[#53635d] hover:text-[#142536] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#78b892]">{label}<Icon className="h-3.5 w-3.5" /></button>;
}

export function TransactionTable({ records, loading, filters, onSort, onSelect }: Props) {
  if (loading) return <div className="flex min-h-80 items-center justify-center"><Spinner label="Loading transactions" /></div>;
  if (records.length === 0) return <EmptyState />;
  return <div className="max-w-full overflow-x-auto"><table className="w-full min-w-[760px] border-collapse text-left"><thead className="sticky top-0 z-10 bg-[#f5f7f4] text-xs uppercase tracking-wide text-[#66756f]"><tr><th className="px-4 py-3"><SortButton label="Date" field="timestamp" filters={filters} onSort={onSort} /></th><th className="px-4 py-3">Merchant</th><th className="px-4 py-3">Category</th><th className="px-4 py-3 text-right"><SortButton label="Amount" field="amount" filters={filters} onSort={onSort} /></th><th className="px-4 py-3">Status</th><th className="px-4 py-3">Payment method</th></tr></thead><tbody>{records.map((transaction) => { const amount = Number(transaction.amount); return <tr key={transaction.id} tabIndex={0} role="button" aria-label={`View ${transaction.merchant} transaction details`} onClick={() => onSelect(transaction)} onKeyDown={(event) => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); onSelect(transaction); } }} className="cursor-pointer border-t border-[#edf0ed] text-sm text-[#34444e] transition hover:bg-[#f5faf6] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-[#78b892]"><td className="whitespace-nowrap px-4 py-3.5">{dateTime.format(new Date(transaction.timestamp))}</td><td className="px-4 py-3.5 font-semibold text-[#1c2b35]">{transaction.merchant}<span className="mt-0.5 block font-mono text-xs font-normal text-[#7b8983]">{transaction.source_transaction_id}</span></td><td className="px-4 py-3.5">{transaction.category ?? "Uncategorized"}</td><td className={`px-4 py-3.5 text-right font-bold ${amount < 0 ? "text-[#b74848]" : "text-[#1c2b35]"}`}>{currency.format(amount)}</td><td className="px-4 py-3.5"><Badge status={transaction.status} /></td><td className="px-4 py-3.5">{transaction.payment_method}</td></tr>; })}</tbody></table></div>;
}
