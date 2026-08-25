import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Coinly | Financial dashboard",
  description: "A clearer view of spending and rewards.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
