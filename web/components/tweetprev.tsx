"use client";

// import Comment from "pixelarticons/svg/comment.svg"
// import Like from "pixelarticons/svg/heart.svg"

export function TweetPreview(props: {
  name: string;
  handle: string;
  content: string;
  replies: number;
  likes: number;
}) {
  return (
    <div
      className="flex flex-row w-full p-2 gap-2
      border-t-[3px] border-l-[3px] border-l-[#fcfcfc] border-t-[#fcfcfc]
      active:border-l-[#484848] active:border-t-[#484848]
      border-b-[3px] border-r-[3px] border-b-[#484848] border-r-[#484848]
      active:border-b-[#fcfcfc] active:border-r-[#fcfcfc]
                  "
    >
      <div className="">
        <div className="overflow-hidden bg-purple-400 w-10 h-10"></div>
      </div>
      <div className="flex flex-col w-full">
        <div className="flex flex-row gap-3">
          <p className="font-bold">{props.name}</p>
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
