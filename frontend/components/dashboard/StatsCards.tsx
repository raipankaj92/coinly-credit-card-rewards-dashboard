import { CircleCheck, ReceiptText, TrendingUp, Wallet } from "lucide-react";
import { Card } from "@/components/ui/Card";

type Props = { totalSpending: number; successfulTransactions: number; coinBalance?: number; transactionCount: number };
const currency = new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 });

export function StatsCards({ totalSpending, successfulTransactions, coinBalance, transactionCount }: Props) {
  const cards = [
    { label: "Net spending", value: currency.format(totalSpending), icon: TrendingUp, note: "Signed source total" },
    { label: "Successful payments", value: successfulTransactions.toLocaleString("en-IN"), icon: CircleCheck, note: "Completed transactions" },
    { label: "Coin balance", value: coinBalance?.toLocaleString("en-IN") ?? "...", icon: Wallet, note: "Available to redeem" },
    { label: "Transactions", value: transactionCount.toLocaleString("en-IN"), icon: ReceiptText, note: "All recorded activity" },
  ];
  return <section aria-label="Dashboard summary" className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">{cards.map(({ label, value, icon: Icon, note }) => <Card key={label} className="p-5"><div className="flex items-start justify-between"><div><p className="text-sm font-medium text-[#66756f]">{label}</p><p className="mt-2 text-2xl font-bold text-[#142536]">{value}</p></div><span className="rounded-md bg-[#e8f2eb] p-2.5 text-[#367050]"><Icon className="h-5 w-5" /></span></div><p className="mt-3 text-xs text-[#84908b]">{note}</p></Card>)}</section>;
}
