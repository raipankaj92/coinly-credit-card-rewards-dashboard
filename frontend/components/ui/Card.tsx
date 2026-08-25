import type { HTMLAttributes, ReactNode } from "react";

export function Card({ children, className = "", ...props }: HTMLAttributes<HTMLDivElement> & { children: ReactNode }) {
  return (
    <section className={`rounded-lg border border-[#dfe4df] bg-white shadow-panel ${className}`} {...props}>
      {children}
    </section>
  );
}
