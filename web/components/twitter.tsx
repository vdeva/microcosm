import React, { useState, useEffect, useRef } from 'react';
import { TweetPreview } from "./tweetprev";

export function Twitter() {
  const [tweets, setTweets] = useState([]);
  const tweetContainerRef = useRef(null); // Create a ref for the tweet container

  // Function to fetch tweets
  const fetchTweets = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/twitterfeed');
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
    <div className="flex flex-col w-[400px] h-[500px] bg-[#c3c3c3]
              ">
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
