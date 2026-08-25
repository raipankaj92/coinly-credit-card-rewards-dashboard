export function Spinner({ label = "Loading", className = "" }: { label?: string; className?: string }) {
  return <span role="status" aria-label={label} className={`inline-block h-5 w-5 animate-spin rounded-full border-2 border-[#c9d1cb] border-t-[#4a7f62] ${className}`} />;
}
