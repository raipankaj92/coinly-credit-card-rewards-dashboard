"use client";

import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { MonthlySpending } from "@/lib/types";
import { Card } from "@/components/ui/Card";
import { EmptyState } from "@/components/ui/EmptyState";
import { Spinner } from "@/components/ui/Spinner";

const currency = new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0, notation: "compact" });

export function MonthlySpending({ data, loading, onSelect }: { data: MonthlySpending[]; loading: boolean; onSelect: (month: string) => void }) {
  const chartData = data.map((item) => ({ ...item, total: Number(item.total), label: new Intl.DateTimeFormat("en-IN", { month: "short", year: "2-digit" }).format(new Date(`${item.month}-01T00:00:00Z`)) }));
  return <Card className="min-h-[340px] p-5"><div className="mb-3"><p className="text-base font-bold text-[#142536]">Monthly spending trend</p><p className="mt-1 text-sm text-[#6b7a74]">Select a month to focus the table</p></div>{loading ? <div className="grid min-h-60 place-items-center"><Spinner label="Loading monthly spending" /></div> : chartData.length === 0 ? <EmptyState title="No monthly data" description="There is no spending data to chart." /> : <div className="h-64"><ResponsiveContainer width="100%" height="100%"><AreaChart data={chartData} onClick={(state) => { const month = state?.activePayload?.[0]?.payload?.month; if (typeof month === "string") onSelect(month); }} margin={{ left: -18, right: 8 }}><defs><linearGradient id="spendingArea" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#4a7f62" stopOpacity={0.34} /><stop offset="100%" stopColor="#4a7f62" stopOpacity={0.02} /></linearGradient></defs><CartesianGrid vertical={false} stroke="#e5eae6" /><XAxis dataKey="label" tickLine={false} axisLine={false} tick={{ fontSize: 11, fill: "#718078" }} /><YAxis tickFormatter={(value) => currency.format(value)} tickLine={false} axisLine={false} tick={{ fontSize: 11, fill: "#718078" }} /><Tooltip formatter={(value) => new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR" }).format(Number(value))} /><Area type="monotone" dataKey="total" stroke="#3e7657" strokeWidth={2} fill="url(#spendingArea)" /></AreaChart></ResponsiveContainer></div>}</Card>;
}
