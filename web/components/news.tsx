"use client";

import React, { useState, useEffect, useRef } from "react";
import { TweetPreview } from "./tweetprev";
import Image from "next/image";

export function News() {
  function ExpandableText({ text, limit = 500 }) {
    const [isExpanded, setIsExpanded] = useState(false);

    // Ensure 'text' is treated as a string
    const content = text.toString();

    if (content.length <= limit) {
      return <p className="text-sm text-gray-600">{content}</p>;
    }

    return (
      <div>
        <p className="text-sm text-gray-600">
          {isExpanded ? content : `${content.substring(0, limit)}...`}
        </p>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-blue-500 hover:text-blue-800"
        >
          {isExpanded ? "Read Less" : "Read More..."}
        </button>
      </div>
    );
  }

  const [articles, setArticles] = useState([]);

  // Fetch articles from the server on component mount
  useEffect(() => {
    fetch("http://127.0.0.1:8000/recent-articles")
      .then((response) => response.json())
      .then((data) => setArticles(data))
      .catch((error) =>
        console.error("There was an error fetching the articles:", error),
      );
  }, []); // Empty dependency array to run only once on mount

  return (
    <div
      className="flex flex-col w-[600px] h-[500px] bg-[#ffffff]
    border-t-[3px] border-l-[3px] border-b-[#fcfcfc] border-r-[#fcfcfc]
    border-b-[3px] border-r-[3px] border-l-[#484848] border-t-[#484848]"
    >
      <div className="flex flex-row justify-between items-center pt-5 px-5">
        <div className="">{`Today's Paper`}</div>
        <Image
          src="/mstimes.png"
          alt="the mistral times"
          width={280}
          height={0}
        />
        <div className=" text-end">
          {new Date(Date.now()).toLocaleDateString()}
        </div>
      </div>
      <div className="w-full px-3">
        <div className="h-[1px] w-full bg-neutral-600 mt-3" />
      </div>
      <div className="flex flex-col items-center overflow-y-auto">
        {articles.map((article, index) => (
          <div key={index} className="p-5 border-b border-gray-200 w-full">
            <h3 className="text-lg font-semibold">{article.title}</h3>
            <ExpandableText text={article.content} />
          </div>
        ))}
      </div>
    </div>
  );
}
