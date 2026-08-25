import type { ButtonHTMLAttributes, ReactNode } from "react";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "ghost" | "danger";
  children: ReactNode;
};

const variants = {
  primary: "bg-[#142536] text-white hover:bg-[#1d354b] focus-visible:ring-[#78b892]",
  secondary: "border border-[#d7ddd8] bg-white text-[#142536] hover:bg-[#f2f5f2] focus-visible:ring-[#78b892]",
  ghost: "text-[#40515d] hover:bg-[#edf1ee] focus-visible:ring-[#78b892]",
  danger: "bg-[#b74848] text-white hover:bg-[#963a3a] focus-visible:ring-[#b74848]",
};

export function Button({ variant = "primary", className = "", children, ...props }: ButtonProps) {
  return (
    <button
      className={`inline-flex min-h-10 items-center justify-center gap-2 rounded-md px-4 text-sm font-semibold transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
