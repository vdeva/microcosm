"use client";

import Image from "next/image";

export default function ThankYou() {
  return (
    <main className="flex flex-col h-screen w-full justify-center items-center">
      <Image src={"/ty.png"} alt="thank you" width={800} height={0}></Image>
    </main>
  );
}
