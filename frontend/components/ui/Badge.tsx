import type { TransactionStatus } from "@/lib/types";

const styles: Record<TransactionStatus, string> = {
  SUCCESS: "bg-[#e5f3e9] text-[#27633c] ring-[#b8dabe]",
  PENDING: "bg-[#fff4d9] text-[#8a6114] ring-[#edd391]",
  FAILED: "bg-[#fde8e7] text-[#a13e38] ring-[#efbbb6]",
};

export function Badge({ status }: { status: TransactionStatus }) {
  return <span className={`inline-flex rounded-full px-2.5 py-1 text-xs font-bold ring-1 ring-inset ${styles[status]}`}>{status}</span>;
}
