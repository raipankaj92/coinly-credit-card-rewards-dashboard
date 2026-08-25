"use client";

import { X } from "lucide-react";
import { useEffect, useRef, type ReactNode } from "react";

type ModalProps = {
  open: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
  size?: "md" | "lg";
};

export function Modal({ open, onClose, title, children, size = "md" }: ModalProps) {
  const closeRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (!open) return;
    closeRef.current?.focus();
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [onClose, open]);

  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-end bg-[#10202b]/45 p-0 sm:items-center sm:justify-center sm:p-6" role="presentation" onMouseDown={onClose}>
      <section aria-modal="true" aria-labelledby="modal-title" role="dialog" onMouseDown={(event) => event.stopPropagation()} className={`w-full rounded-t-xl bg-white shadow-2xl sm:rounded-xl ${size === "lg" ? "max-w-3xl" : "max-w-lg"}`}>
        <header className="flex items-center justify-between border-b border-[#e1e6e2] px-5 py-4 sm:px-6"><h2 id="modal-title" className="text-lg font-bold text-[#142536]">{title}</h2><button ref={closeRef} type="button" aria-label="Close modal" onClick={onClose} className="rounded-md p-2 text-[#52635e] hover:bg-[#edf1ee] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#78b892]"><X className="h-5 w-5" /></button></header>
        {children}
      </section>
    </div>
  );
}
