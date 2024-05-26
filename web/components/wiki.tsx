"use client";

import React, { useState, useEffect } from "react";
import Image from "next/image";
import { WikiRender } from "./wikirender";

export function Wiki() {
  const [wikipages, setWikipages] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(false); // Added isLoading state

  // Fetch wikipages from the server on component mount
  useEffect(() => {
    fetch("http://127.0.0.1:8000/recent-wikipages")
      .then((response) => response.json())
      .then((data) => setWikipages(data))
      .catch((error) =>
        console.error("There was an error fetching the wikipages:", error),
      );
  }, []);

  function handleSearch(e) {
    e.preventDefault();
    if (!searchTerm.trim()) return; // Prevent search if input is empty
    setIsLoading(true); // Set loading to true when search starts

    fetch(
      `http://127.0.0.1:8000/generate-wiki?query=${encodeURIComponent(searchTerm)}`,
    )
      .then((response) => response.json())
      .then((data) => {
        setWikipages([data, ...wikipages]); // Prepend new wikipage to the current list
        setSearchTerm(""); // Reset search term
        setIsLoading(false); // Set loading to false when search is complete
      })
      .catch((error) => {
        console.error("There was an error fetching the search results:", error);
        setIsLoading(false); // Ensure loading is false if fetch fails
      });
  }

  return (
    <div
      className="flex flex-col w-[600px] h-[500px] bg-[#ffffff]
    border-t-[3px] border-l-[3px] border-b-[#fcfcfc] border-r-[#fcfcfc]
    border-b-[3px] border-r-[3px] border-l-[#484848] border-t-[#484848] overflow-y-auto font-black"
    >
      <div className="flex flex-col justify-center items-center py-12 px-5 gap-6">
        <Image src="/wiki.png" alt="WikiLlama" width={200} height={200} />
        <p className="text-4xl">WikiLlama</p>
        <form onSubmit={handleSearch} className="w-full px-6">
          <input
            type="text"
            placeholder="Search..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full p-2 border border-gray-300"
            disabled={isLoading}
          />
          <button type="submit" className="hidden">
            Search
          </button>
        </form>
      </div>
      <div className="w-full px-3">
        <div className="h-[1px] w-full bg-neutral-600 mt-3" />
      </div>
      <div className="flex flex-col items-center">
        {wikipages.map((wikipage, index) => (
          <div key={index} className="p-5 border-b border-gray-200 w-full">
            <h3 className="text-lg font-semibold">{wikipage.title}</h3>
            <WikiRender contents={wikipage.content} />
          </div>
        ))}
      </div>
    </div>
  );
}
