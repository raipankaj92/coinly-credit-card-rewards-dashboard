import { SearchX } from "lucide-react";

export function EmptyState({ title = "No transactions found", description = "Try changing or clearing your filters." }: { title?: string; description?: string }) {
  return <div className="flex min-h-52 flex-col items-center justify-center px-6 text-center"><SearchX className="mb-3 h-7 w-7 text-[#789084]" /><p className="font-semibold text-[#263641]">{title}</p><p className="mt-1 text-sm text-[#6c7b75]">{description}</p></div>;
}
