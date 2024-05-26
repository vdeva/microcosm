import type { Metadata } from "next";
import localFont from "next/font/local";
import "@/styles/globals.css";

const myFont = localFont({
  src: [
    {
      path: "./fonts/scientifica.woff2",
      weight: "400",
      style: "normal",
    },
    {
      path: "./fonts/scientificaItalic.woff2",
      weight: "400",
      style: "italic",
    },
    {
      path: "./fonts/scientificaBold.woff2",
      weight: "700",
      style: "normal",
    },
    {
      path: "./fonts/Dico.woff2",
      weight: "900",
      style: "normal",
    },
  ],
});

export const metadata: Metadata = {
  title: "microcosm",
  description: "computer from another world",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={myFont.className}>{children}</body>
    </html>
  );
}
