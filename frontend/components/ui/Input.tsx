import type { InputHTMLAttributes } from "react";

export function Input({ className = "", ...props }: InputHTMLAttributes<HTMLInputElement>) {
  return <input className={`min-h-10 w-full rounded-md border border-[#cfd7d1] bg-white px-3 text-sm text-[#1b2934] outline-none placeholder:text-[#82908a] focus:border-[#4a7f62] focus:ring-2 focus:ring-[#cfe6d5] ${className}`} {...props} />;
}
