"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";
import type { Pagination } from "@/lib/types";
import { Button } from "@/components/ui/Button";

export function TransactionPagination({ pagination, onPageChange }: { pagination: Pagination; onPageChange: (page: number) => void }) {
  const start = pagination.total === 0 ? 0 : (pagination.page - 1) * pagination.page_size + 1;
  const end = Math.min(pagination.page * pagination.page_size, pagination.total);
  return <footer className="flex flex-col gap-3 border-t border-[#e1e6e2] px-4 py-4 sm:flex-row sm:items-center sm:justify-between"><p className="text-sm text-[#66756f]">Showing {start}-{end} of {pagination.total.toLocaleString("en-IN")}</p><div className="flex items-center gap-2"><Button variant="secondary" aria-label="Previous page" disabled={pagination.page <= 1} onClick={() => onPageChange(pagination.page - 1)} className="min-h-9 px-3"><ChevronLeft className="h-4 w-4" /></Button><span className="min-w-24 text-center text-sm font-semibold text-[#354651]">Page {pagination.page} of {pagination.total_pages || 1}</span><Button variant="secondary" aria-label="Next page" disabled={pagination.page >= pagination.total_pages} onClick={() => onPageChange(pagination.page + 1)} className="min-h-9 px-3"><ChevronRight className="h-4 w-4" /></Button></div></footer>;
}
