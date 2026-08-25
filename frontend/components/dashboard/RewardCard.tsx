import { Gift, Ticket } from "lucide-react";
import type { Reward } from "@/lib/types";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";

export function RewardCard({ reward, balance, onRedeem }: { reward: Reward; balance?: number; onRedeem: (reward: Reward) => void }) {
  const affordable = balance !== undefined && balance >= reward.coin_cost;
  return <Card className="flex min-h-56 flex-col p-5"><div className="flex items-start justify-between gap-3"><span className="grid h-10 w-10 shrink-0 place-items-center rounded-md bg-[#e8f2eb] text-[#367050]"><Gift className="h-5 w-5" /></span><span className="rounded-full bg-[#f0f3f0] px-2.5 py-1 text-xs font-bold text-[#52635e]">{reward.reward_type}</span></div><h3 className="mt-4 font-bold text-[#142536]">{reward.name}</h3><p className="mt-1 text-sm leading-5 text-[#66756f]">{reward.description}</p><div className="mt-auto flex items-center justify-between gap-3 pt-5"><span className="inline-flex items-center gap-1.5 text-sm font-bold text-[#367050]"><Ticket className="h-4 w-4" />{reward.coin_cost.toLocaleString("en-IN")} coins</span><Button onClick={() => onRedeem(reward)} disabled={!reward.active || balance === undefined || !affordable} aria-label={`Redeem ${reward.name}`}>Redeem</Button></div>{balance !== undefined && !affordable && <p className="mt-2 text-xs text-[#8a6114]">Need {(reward.coin_cost - balance).toLocaleString("en-IN")} more coins</p>}</Card>;
}
