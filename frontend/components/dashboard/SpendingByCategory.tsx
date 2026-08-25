"use client";

import { Pie, PieChart, Cell, ResponsiveContainer, Tooltip } from "recharts";
import type { CategorySpending } from "@/lib/types";
import { Card } from "@/components/ui/Card";
import { EmptyState } from "@/components/ui/EmptyState";
import { Spinner } from "@/components/ui/Spinner";

const COLORS = ["#4a7f62", "#d58b4d", "#477d92", "#9b6a71", "#8b9b52", "#776f9e", "#bc6e58", "#5d8c83", "#b4984d", "#6f7e9a", "#777b74"];
const currency = new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 });

export function SpendingByCategory({ data, loading, onSelect }: { data: CategorySpending[]; loading: boolean; onSelect: (category: string) => void }) {
  const chartData = data.map((item) => ({ ...item, total: Number(item.total) }));
  return <Card className="min-h-[340px] p-5"><div className="mb-3"><p className="text-base font-bold text-[#142536]">Spending by category</p><p className="mt-1 text-sm text-[#6b7a74]">Signed totals from all recorded transactions</p></div>{loading ? <div className="grid min-h-60 place-items-center"><Spinner label="Loading category spending" /></div> : chartData.length === 0 ? <EmptyState title="No category data" description="There is no spending data to chart." /> : <div className="h-64"><ResponsiveContainer width="100%" height="100%"><PieChart><Pie data={chartData} dataKey="total" nameKey="category" innerRadius="54%" outerRadius="82%" paddingAngle={2} onClick={(entry) => onSelect(entry.category)}>{chartData.map((item, index) => <Cell key={item.category} fill={COLORS[index % COLORS.length]} className="cursor-pointer outline-none" />)}</Pie><Tooltip formatter={(value) => currency.format(Number(value))} /></PieChart></ResponsiveContainer></div>}<div className="mt-3 grid grid-cols-2 gap-x-3 gap-y-2 text-xs">{chartData.slice(0, 6).map((item, index) => <button type="button" key={item.category} onClick={() => onSelect(item.category)} className="flex items-center gap-2 text-left text-[#586963] hover:text-[#142536]"><span className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: COLORS[index % COLORS.length] }} /><span className="truncate">{item.category}</span></button>)}</div></Card>;
}
