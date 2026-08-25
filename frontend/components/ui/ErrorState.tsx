import { AlertCircle } from "lucide-react";
import { Button } from "./Button";

export function ErrorState({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return <div className="flex min-h-52 flex-col items-center justify-center px-6 text-center"><AlertCircle className="mb-3 h-7 w-7 text-[#b74848]" /><p className="max-w-md text-sm text-[#75413e]">{message}</p>{onRetry && <Button className="mt-4" variant="secondary" onClick={onRetry}>Try again</Button>}</div>;
}
