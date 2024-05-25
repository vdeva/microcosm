"use client";

import { News } from "@/components/news";
import { Twitter } from "@/components/twitter";
import Image from "next/image";
import { useState } from "react";
import Draggable from "react-draggable";

export default function Home() {
  const [isTwitterOpen, setIsTwitterOpen] = useState(false);
  const [isNewsOpen, setIsNewsOpen] = useState(false);

  return (
    <main className="flex flex-col h-screen w-full">
      <div className="w-full h-full bg-[#008282] z-0">
        <div className="absolute flex flex-row justify-between">
          <div className="flex flex-col items-center gap-7 pl-7 pt-7">
            <button
              className="flex flex-col gap-1 items-center p-3 w-[100px]
            border-2 border-transparent hover:border-sky-400 border-dotted"
              onClick={() => setIsTwitterOpen(true)}
            >
              <Image
                src={"/twitter.png"}
                alt="twitter logo"
                width={48}
                height={48}
              />
              <p className="text-white">Twitter</p>
            </button>
            <button
              className="flex flex-col gap-1 items-center p-3 w-[100px]
            border-2 border-transparent hover:border-sky-400 border-dotted"
              onClick={() => setIsNewsOpen(true)}
            >
              <Image
                src={"/news.png"}
                alt="news logo"
                width={58}
                height={58}
              />
              <p className="text-white">News</p>
            </button>
            <button
              className="flex flex-col gap-1 items-center p-3 w-[100px]
            border-2 border-transparent hover:border-sky-400 border-dotted"
              onClick={() => setIsNewsOpen(true)}
            >
              <Image
                src={"/trade.png"}
                alt="trade logo"
                width={58}
                height={58}
              />
              <p className="text-white">Market</p>
            </button>
            <button
              className="flex flex-col gap-1 items-center p-3 w-[100px]
            border-2 border-transparent hover:border-sky-400 border-dotted"
              onClick={() => setIsNewsOpen(true)}
            >
              <Image
                src={"/wiki.png"}
                alt="wiki logo"
                width={58}
                height={58}
              />
              <p className="text-white">Wiki</p>
            </button>
          </div>
        </div>
        {isTwitterOpen && (
          <div className="max-h-min max-w-min z-10 inset-0 absolute pointer-events-none">
            <Draggable
              cancel=".no-drag"
              positionOffset={{ x: "300px", y: "100px" }}
            >
              <div
                className="bg-[#c3c3c3] pointer-events-auto
              flex flex-col
              border-t-[3px] border-l-[3px] border-l-[#fcfcfc] border-t-[#fcfcfc]
              border-b-[3px] border-r-[3px] border-b-[#484848] border-r-[#484848]
              "
              >
                <div className=" select-none h-8 bg-[#000082] flex flex-row items-center pl-2 pr-1 justify-between">
                  <p className="text-white text-lg">Twitter</p>
                  <button
                    className=" no-drag
                  bg-[#c3c3c3] h-6 w-6
                  flex flex-col items-center justify-center p-1
                  border-t-[3px] border-l-[3px] border-l-[#fcfcfc] border-t-[#fcfcfc]
                  active:border-l-[#484848] active:border-t-[#484848]
                  border-b-[3px] border-r-[3px] border-b-[#484848] border-r-[#484848]
                  active:border-b-[#fcfcfc] active:border-r-[#fcfcfc]
                  text-center
                  "
                    onClick={() => setIsTwitterOpen(false)}
                  >
                    ⨯
                  </button>
                </div>
                <div className="no-drag">
                  <Twitter />
                </div>
              </div>
            </Draggable>
          </div>
        )}
        {isNewsOpen && (
          <div className="max-h-min max-w-min z-10 inset-0 absolute pointer-events-none">
            <Draggable
              cancel=".no-drag"
              positionOffset={{ x: "300px", y: "100px" }}
            >
              <div
                className="bg-[#c3c3c3] pointer-events-auto
              flex flex-col
              border-t-[3px] border-l-[3px] border-l-[#fcfcfc] border-t-[#fcfcfc]
              border-b-[3px] border-r-[3px] border-b-[#484848] border-r-[#484848]
              "
              >
                <div className=" select-none h-8 bg-[#000082] flex flex-row items-center pl-2 pr-1 justify-between">
                  <p className="text-white text-lg">News</p>
                  <button
                    className=" no-drag
                  bg-[#c3c3c3] h-6 w-6
                  flex flex-col items-center justify-center p-1
                  border-t-[3px] border-l-[3px] border-l-[#fcfcfc] border-t-[#fcfcfc]
                  active:border-l-[#484848] active:border-t-[#484848]
                  border-b-[3px] border-r-[3px] border-b-[#484848] border-r-[#484848]
                  active:border-b-[#fcfcfc] active:border-r-[#fcfcfc]
                  text-center
                  "
                    onClick={() => setIsNewsOpen(false)}
                  >
                    ⨯
                  </button>
                </div>
                <div className="no-drag">
                  <News />
                </div>
              </div>
            </Draggable>
          </div>
        )}
      </div>
      <div
        className="flex flex-row items-center z-40
      gap-2 bg-[#c3c3c3]
      border-t-2 border-t-[#fcfcfc]
      px-2 py-2"
      >
        <button
          className="flex flex-row items-center bg-[#c3c3c3] px-4 py-2
        border-t-[3px] border-l-[3px] border-l-[#fcfcfc] border-t-[#fcfcfc]
        active:border-l-[#484848] active:border-t-[#484848]
        border-b-[3px] border-r-[3px] border-b-[#484848] border-r-[#484848]
        active:border-b-[#fcfcfc] active:border-r-[#fcfcfc]
        max-h-9"
        >
          <p className="font-bold text-lg select-none">{`Start`}</p>
        </button>
        {isTwitterOpen && (
          <button
            className="flex flex-row items-center bg-[#c3c3c3] px-4 py-2
          border-t-[3px] border-l-[3px] border-l-[#fcfcfc] border-t-[#fcfcfc]
          active:border-l-[#484848] active:border-t-[#484848]
          border-b-[3px] border-r-[3px] border-b-[#484848] border-r-[#484848]
          active:border-b-[#fcfcfc] active:border-r-[#fcfcfc]
          max-h-9"
          >
            <p className="font-bold text-lg select-none">{`Twitter`}</p>
          </button>
        )}
        {isNewsOpen && (
          <button
            className="flex flex-row items-center bg-[#c3c3c3] px-4 py-2
          border-t-[3px] border-l-[3px] border-l-[#fcfcfc] border-t-[#fcfcfc]
          active:border-l-[#484848] active:border-t-[#484848]
          border-b-[3px] border-r-[3px] border-b-[#484848] border-r-[#484848]
          active:border-b-[#fcfcfc] active:border-r-[#fcfcfc]
          max-h-9"
          >
            <p className="font-bold text-lg select-none">{`News`}</p>
          </button>
        )}
      </div>
    </main>
  );
}
