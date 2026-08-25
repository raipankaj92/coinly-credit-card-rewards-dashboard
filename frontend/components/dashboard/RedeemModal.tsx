import { CheckCircle2 } from "lucide-react";
import type { Reward } from "@/lib/types";
import { Button } from "@/components/ui/Button";
import { Modal } from "@/components/ui/Modal";
import { Spinner } from "@/components/ui/Spinner";

type Props = { reward: Reward | null; balance?: number; loading: boolean; error?: string; success?: boolean; onClose: () => void; onConfirm: () => void };

export function RedeemModal({ reward, balance, loading, error, success, onClose, onConfirm }: Props) {
  if (!reward) return null;
  return <Modal open={Boolean(reward)} onClose={loading ? () => undefined : onClose} title={success ? "Reward redeemed" : "Confirm redemption"}><div className="p-5 sm:p-6">{success ? <div className="text-center"><CheckCircle2 className="mx-auto h-11 w-11 text-[#367050]" /><p className="mt-3 font-semibold text-[#142536]">{reward.name} is yours.</p><p className="mt-1 text-sm text-[#66756f]">Your updated balance is {balance?.toLocaleString("en-IN")} coins.</p><Button className="mt-5" onClick={onClose}>Done</Button></div> : <><p className="text-sm leading-6 text-[#52635e]">Redeem <strong className="text-[#142536]">{reward.name}</strong> for {reward.coin_cost.toLocaleString("en-IN")} coins?</p><div className="mt-4 rounded-md bg-[#f3f6f3] p-3 text-sm text-[#52635e]">Current balance <strong className="float-right text-[#142536]">{balance?.toLocaleString("en-IN")} coins</strong></div>{error && <p role="alert" className="mt-3 rounded-md bg-[#fde8e7] p-3 text-sm text-[#a13e38]">{error}</p>}<div className="mt-5 flex justify-end gap-3"><Button variant="ghost" disabled={loading} onClick={onClose}>Cancel</Button><Button disabled={loading} onClick={onConfirm}>{loading && <Spinner className="h-4 w-4 border-2" />}Confirm redeem</Button></div></>}</div></Modal>;
}
