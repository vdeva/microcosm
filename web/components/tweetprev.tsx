"use client";

import Image from "next/image";

// import Comment from "pixelarticons/svg/comment.svg"
// import Like from "pixelarticons/svg/heart.svg"

export function TweetPreview(props: {
  id: number;
  name: string;
  handle: string;
  content: string;
  replies: number;
  likes: number;
}) {
  return (
    <div
      className="flex flex-row w-full p-4 gap-4 bg-neutral-200
      border-t-[3px] border-l-[3px] border-l-[#fcfcfc] border-t-[#fcfcfc]
      active:border-l-[#484848] active:border-t-[#484848]
      border-b-[3px] border-r-[3px] border-b-[#484848] border-r-[#484848]
      active:border-b-[#fcfcfc] active:border-r-[#fcfcfc]
                  "
    >
      <div className="">
        <img
          className="pixel-art"
          src={`/punks/${props.id}.png`}
          alt="pfp"
          width={52}
          height={52}
        />
      </div>
      <div className="flex flex-col w-full">
        <div className="flex flex-row gap-3 items-baseline">
          <p className="font-bold text-lg">{props.name}</p>
          <p>@{props.handle}</p>
          {/* <p>{props.time.toLocaleTimeString()}</p> */}
        </div>
        <p>{props.content}</p>
        <div className="flex flex-row w-full gap-8 text-sm mt-3">
          <div className="flex flex-row items-center gap-1">
            Replies:
            <p>{props.replies}</p>
          </div>
          <div className="flex flex-row items-center gap-1">
            Likes:
            <p>{props.likes}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
