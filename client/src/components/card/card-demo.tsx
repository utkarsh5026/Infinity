"use client";

import { useState } from "react";
import { LearningCard } from "./learning-card";
// Mock learning content with markdown
const mockLearningCards = [
  {
    id: 1,
    topic: "JavaScript Async/Await",
    category: "Programming",
    difficulty: "Intermediate",
    timeToRead: "3 min",
    question:
      "## Understanding Async/Await in JavaScript\n\nWhat is async/await and how does it improve upon traditional Promise handling?",
    answer: `**Async/await** is syntactic sugar built on top of Promises that makes asynchronous code look and behave more like synchronous code.

### Key Benefits:
- **Cleaner syntax** - No more Promise chains
- **Better error handling** - Use try/catch blocks
- **Improved readability** - Code reads top to bottom

### Example:
\`\`\`javascript
// Traditional Promise approach
function fetchUserData() {
  return fetch('/api/user')
    .then(response => response.json())
    .then(data => {
      console.log(data);
      return data;
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

// Async/await approach
async function fetchUserData() {
  try {
    const response = await fetch('/api/user');
    const data = await response.json();
    console.log(data);
    return data;
  } catch (error) {
    console.error('Error:', error);
  }
}
\`\`\``,
    explanation: `### Deep Dive: How Async/Await Works

**Under the hood**, async/await is just **syntactic sugar** for Promises. When you use \`async\`, the function automatically returns a Promise.

#### Key Concepts:
1. **Async Functions** always return a Promise
2. **Await** can only be used inside async functions
3. **Error Handling** uses traditional try/catch syntax
4. **Sequential vs Parallel** execution patterns

#### Best Practices:
- Use \`Promise.all()\` for parallel operations
- Don't forget error handling with try/catch
- Be mindful of blocking behavior with await`,
    xp: 25,
    tags: ["javascript", "promises", "async", "es2017"],
  },
  {
    id: 2,
    topic: "React useEffect Hook",
    category: "React",
    difficulty: "Beginner",
    timeToRead: "2 min",
    question:
      "## React useEffect Hook\n\nWhen and why should you use the useEffect hook in React functional components?",
    answer: `**useEffect** is React's way of handling side effects in functional components. It replaces lifecycle methods from class components.

### Common Use Cases:
- **Data fetching** from APIs
- **Setting up subscriptions** or event listeners
- **Manually updating the DOM**
- **Cleanup operations**

### Basic Syntax:
\`\`\`javascript
import { useEffect, useState } from 'react';

function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Side effect: fetch user data
    fetchUser(userId)
      .then(setUser);

    // Optional cleanup
    return () => {
      // Cleanup code here
    };
  }, [userId]); // Dependency array

  return <div>{user?.name}</div>;
}
\`\`\``,
    explanation: `### Understanding useEffect Dependencies

The **dependency array** is crucial for performance and correctness:

- **Empty array \`[]\`** - Effect runs once after mount
- **No array** - Effect runs after every render
- **With dependencies \`[value]\`** - Effect runs when dependencies change

#### Memory Leaks Prevention:
Always cleanup subscriptions, timers, and event listeners in the return function to prevent memory leaks.`,
    xp: 20,
    tags: ["react", "hooks", "useeffect", "lifecycle"],
  },
];

const LearningCardDemo = () => {
  const [currentCardIndex, setCurrentCardIndex] = useState(0);

  const handleSwipe = (direction) => {
    console.log(`Swiped ${direction}`);

    if (direction === "up" || direction === "left") {
      setCurrentCardIndex((prev) =>
        prev < mockLearningCards.length - 1 ? prev + 1 : 0
      );
    } else if (direction === "down") {
      setCurrentCardIndex((prev) =>
        prev > 0 ? prev - 1 : mockLearningCards.length - 1
      );
    }
  };

  const handleComplete = (card) => {
    console.log("Completed card:", card.topic);
    // Here you would typically update progress, award XP, etc.
    handleSwipe("up"); // Move to next card
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-4">
      <div className="max-w-md mx-auto">
        {/* Header */}
        <div className="text-center mb-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Interactive Learning Cards
          </h1>
          <p className="text-gray-600">
            Swipe to navigate • Tap to reveal content
          </p>
        </div>

        {/* Card */}
        <LearningCard
          card={mockLearningCards[currentCardIndex]}
          onSwipe={handleSwipe}
          onComplete={handleComplete}
        />

        {/* Card Counter */}
        <div className="text-center mt-4">
          <span className="text-sm text-gray-500">
            {currentCardIndex + 1} of {mockLearningCards.length}
          </span>
        </div>
      </div>
    </div>
  );
};

export default LearningCardDemo;
