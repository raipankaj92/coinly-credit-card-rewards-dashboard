import type { Reward } from "@/lib/types";
import { ErrorState } from "@/components/ui/ErrorState";
import { Spinner } from "@/components/ui/Spinner";
import { RewardCard } from "./RewardCard";

export function RewardsSection({ rewards, balance, loading, error, onRetry, onRedeem }: { rewards: Reward[]; balance?: number; loading: boolean; error?: string; onRetry: () => void; onRedeem: (reward: Reward) => void }) {
  return <section id="rewards" className="scroll-mt-6"><div className="mb-5 flex flex-wrap items-end justify-between gap-3"><div><p className="text-xs font-bold uppercase tracking-[0.16em] text-[#4a7f62]">Rewards</p><h2 className="mt-1 text-2xl font-bold text-[#142536]">Turn spending into more</h2></div><p className="rounded-md bg-[#e8f2eb] px-3 py-2 text-sm text-[#27633c]">Available balance: <strong>{balance?.toLocaleString("en-IN") ?? "..."} coins</strong></p></div>{loading ? <div className="grid min-h-56 place-items-center"><Spinner label="Loading rewards" /></div> : error ? <ErrorState message={error} onRetry={onRetry} /> : <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">{rewards.map((reward) => <RewardCard key={reward.id} reward={reward} balance={balance} onRedeem={onRedeem} />)}</div>}</section>;
}
