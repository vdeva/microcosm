import React, { useState, useEffect, useRef } from 'react';
import { TweetPreview } from "./tweetprev";

export function News() {
  const [tweets, setTweets] = useState([]);
  const tweetContainerRef = useRef(null); // Create a ref for the tweet container

  // Function to fetch tweets
  const fetchTweets = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/newsfeed');
      if (response.ok) {
        const newTweets = await response.json();
        setTweets(prevTweets => [...newTweets, ...prevTweets]); // Prepend new tweets to existing ones
      } else {
        throw new Error('Failed to fetch tweets');
      }
    } catch (error) {
      console.error('Error fetching tweets:', error);
    }
  };

  // Effect to fetch tweets on mount
  useEffect(() => {
    fetchTweets();
  }, []);

  // Effect to add scroll event listener
  useEffect(() => {
    const handleScroll = () => {
      const { scrollTop } = tweetContainerRef.current;
      if (scrollTop === 0) { // Check if scrolled to the top
        fetchTweets(); // Fetch new tweets
      }
    };

    const tweetContainer = tweetContainerRef.current;
    tweetContainer.addEventListener('scroll', handleScroll);

    // Cleanup the event listener on component unmount
    return () => {
      tweetContainer.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <div className="flex flex-col w-[600px] h-[500px] bg-[#ffffff]
    border-t-[3px] border-l-[3px] border-b-[#fcfcfc] border-r-[#fcfcfc]
    border-b-[3px] border-r-[3px] border-l-[#484848] border-t-[#484848]">
      <div ref={tweetContainerRef} className="flex flex-col p-2 gap-2 overflow-auto">
        {tweets.map(tweet => (
          <TweetPreview
            key={tweet.name + tweet.handle} // Assumed unique identifier for React key
            name={tweet.name}
            handle={tweet.handle}
            content={tweet.content}
            replies={tweet.replies}
            likes={tweet.likes}
          />
        ))}
      </div>
    </div>
  );
}
