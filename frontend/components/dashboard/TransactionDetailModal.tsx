"use client";

import type { Transaction } from "@/lib/types";
import { Modal } from "@/components/ui/Modal";

const currency = new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR" });

export function TransactionDetailModal({ transaction, onClose }: { transaction: Transaction | null; onClose: () => void }) {
  if (!transaction) return null;
  const values = [
    ["Transaction ID", transaction.source_transaction_id], ["Date & time", new Intl.DateTimeFormat("en-IN", { dateStyle: "medium", timeStyle: "short" }).format(new Date(transaction.timestamp))], ["Category", transaction.category ?? "Uncategorized"], ["Amount", currency.format(Number(transaction.amount))], ["Currency", transaction.currency], ["Status", transaction.status], ["Payment method", transaction.payment_method],
  ];
  return <Modal open={Boolean(transaction)} onClose={onClose} title={transaction.merchant}><div className="grid gap-0 p-5 sm:grid-cols-2 sm:p-6">{values.map(([label, value]) => <div key={label} className="border-b border-[#edf0ed] py-3 sm:odd:pr-5 sm:even:pl-5"><p className="text-xs font-semibold uppercase tracking-wide text-[#7c8984]">{label}</p><p className="mt-1 break-words text-sm font-semibold text-[#1d2d37]">{value}</p></div>)}</div></Modal>;
}
