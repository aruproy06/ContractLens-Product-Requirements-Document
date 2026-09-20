import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ContractLens | Cited contract intelligence",
  description: "Contract review and obligation tracking with source-linked citations."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
