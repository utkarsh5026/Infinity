"use client";

import React, { useState, useEffect, useRef } from "react";
import { ChevronUp, BookOpen, Brain, Target, Clock, Zap } from "lucide-react";

// Sample learning data
const learningCards = [
  {
    id: 1,
    subject: "JavaScript",
    category: "Programming",
    question: "What is the difference between 'let' and 'var' in JavaScript?",
    answer:
      "'let' has block scope and cannot be redeclared, while 'var' has function scope and can be redeclared. 'let' also doesn't get hoisted in the same way as 'var'.",
    explanation:
      "This is fundamental to understanding JavaScript's scoping rules and avoiding common bugs.",
    difficulty: "Intermediate",
    estimatedTime: "2 min",
  },
  {
    id: 2,
    subject: "Mathematics",
    category: "Calculus",
    question: "What is the derivative of x²?",
    answer: "2x",
    explanation:
      "Using the power rule: d/dx(xⁿ) = n·xⁿ⁻¹, so d/dx(x²) = 2·x¹ = 2x",
    difficulty: "Beginner",
    estimatedTime: "1 min",
  },
  {
    id: 3,
    subject: "React",
    category: "Programming",
    question: "When should you use useEffect vs useLayoutEffect?",
    answer:
      "Use useEffect for side effects that don't need to block the browser's painting. Use useLayoutEffect when you need to make DOM mutations that the user will see.",
    explanation:
      "useLayoutEffect runs synchronously after all DOM mutations but before the browser paints.",
    difficulty: "Advanced",
    estimatedTime: "3 min",
  },
  {
    id: 4,
    subject: "Psychology",
    category: "Learning",
    question: "What is spaced repetition and why is it effective?",
    answer:
      "Spaced repetition is a learning technique where you review information at increasing intervals. It's effective because it exploits the spacing effect in memory.",
    explanation:
      "This technique helps move information from short-term to long-term memory more efficiently.",
    difficulty: "Intermediate",
    estimatedTime: "2 min",
  },
];

const LearningApp = () => {
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [progress, setProgress] = useState(0);
  const [streak, setStreak] = useState(7);
  const [totalLearned, setTotalLearned] = useState(156);
  const [swipeDirection, setSwipeDirection] = useState<"left" | "right" | null>(
    null
  );
  const [cardState, setCardState] = useState("question"); // 'question', 'answer', 'feedback'
  const [userFeedback, setUserFeedback] = useState<
    "easy" | "medium" | "hard" | null
  >(null); // 'easy', 'medium', 'hard'

  const touchStartRef = useRef({ x: 0, y: 0 });
  const cardRef = useRef(null);

  const currentCard = learningCards[currentCardIndex];

  useEffect(() => {
    setProgress((currentCardIndex / learningCards.length) * 100);
  }, [currentCardIndex]);

  const handleTouchStart = (e: React.TouchEvent<HTMLDivElement>) => {
    touchStartRef.current = {
      x: e.touches[0].clientX,
      y: e.touches[0].clientY,
    };
  };

  const handleTouchEnd = (e: React.TouchEvent<HTMLDivElement>) => {
    const deltaX = e.changedTouches[0].clientX - touchStartRef.current.x;
    const deltaY = e.changedTouches[0].clientY - touchStartRef.current.y;

    // Minimum swipe distance
    const minSwipeDistance = 50;

    if (Math.abs(deltaX) > Math.abs(deltaY)) {
      // Horizontal swipe
      if (Math.abs(deltaX) > minSwipeDistance) {
        if (deltaX > 0) {
          handleSwipeRight(); // Save for later
        } else {
          handleSwipeLeft(); // Mark as learned
        }
      }
    } else {
      // Vertical swipe
      if (Math.abs(deltaY) > minSwipeDistance) {
        if (deltaY > 0) {
          handleSwipeDown(); // Previous card
        } else {
          handleSwipeUp(); // Next card
        }
      }
    }
  };

  const handleSwipeUp = () => {
    if (cardState === "question") {
      setShowAnswer(true);
      setCardState("answer");
    } else if (cardState === "answer") {
      setCardState("feedback");
    } else {
      nextCard();
    }
  };

  const handleSwipeDown = () => {
    if (cardState === "feedback") {
      setCardState("answer");
    } else if (cardState === "answer") {
      setShowAnswer(false);
      setCardState("question");
    } else {
      previousCard();
    }
  };

  const handleSwipeLeft = () => {
    setSwipeDirection("left");
    setTimeout(() => {
      setTotalLearned((prev) => prev + 1);
      nextCard();
      setSwipeDirection(null);
    }, 300);
  };

  const handleSwipeRight = () => {
    setSwipeDirection("right");
    setTimeout(() => {
      // Save for later logic
      nextCard();
      setSwipeDirection(null);
    }, 300);
  };

  const nextCard = () => {
    if (currentCardIndex < learningCards.length - 1) {
      setCurrentCardIndex((prev) => prev + 1);
    } else {
      setCurrentCardIndex(0); // Loop back
    }
    resetCardState();
  };

  const previousCard = () => {
    if (currentCardIndex > 0) {
      setCurrentCardIndex((prev) => prev - 1);
    }
    resetCardState();
  };

  const resetCardState = () => {
    setShowAnswer(false);
    setCardState("question");
    setUserFeedback(null);
  };

  const handleFeedback = (difficulty: "easy" | "medium" | "hard") => {
    setUserFeedback(difficulty);
    if (difficulty === "easy") {
      setStreak((prev) => prev + 1);
    }
    setTimeout(() => {
      nextCard();
    }, 1000);
  };

  const getDifficultyColor = (
    difficulty: "Beginner" | "Intermediate" | "Advanced"
  ) => {
    switch (difficulty) {
      case "Beginner":
        return "bg-green-500/20 text-green-400";
      case "Intermediate":
        return "bg-yellow-500/20 text-yellow-400";
      case "Advanced":
        return "bg-red-500/20 text-red-400";
      default:
        return "bg-blue-500/20 text-blue-400";
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground overflow-hidden">
      {/* Header */}
      <div className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-sm border-b border-border">
        <div className="px-4 py-3">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <Brain className="w-6 h-6 text-primary" />
              <span className="font-semibold">QuickLearn</span>
            </div>
            <div className="flex items-center gap-4 text-sm">
              <div className="flex items-center gap-1">
                <Zap className="w-4 h-4 text-yellow-400" />
                <span>{streak}</span>
              </div>
              <div className="flex items-center gap-1">
                <Target className="w-4 h-4 text-green-400" />
                <span>{totalLearned}</span>
              </div>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="w-full bg-secondary rounded-full h-2">
            <div
              className="bg-primary h-2 rounded-full transition-all duration-300 ease-out"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      </div>

      {/* Main Learning Area */}
      <div className="pt-20 pb-6 px-4 h-screen flex flex-col">
        <div className="flex-1 flex items-center justify-center">
          <div
            ref={cardRef}
            className={`
              w-full max-w-md mx-auto bg-card rounded-2xl border border-border 
              shadow-2xl transition-all duration-300 ease-out transform
              ${swipeDirection === "left" ? "-translate-x-full opacity-0" : ""}
              ${swipeDirection === "right" ? "translate-x-full opacity-0" : ""}
              ${cardState === "answer" ? "scale-105" : ""}
            `}
            onTouchStart={handleTouchStart}
            onTouchEnd={handleTouchEnd}
          >
            <div className="p-6">
              {/* Card Header */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <BookOpen className="w-5 h-5 text-primary" />
                  <span className="text-sm font-medium text-muted-foreground">
                    {currentCard.subject}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span
                    className={`px-2 py-1 rounded-full text-xs ${getDifficultyColor(
                      currentCard.difficulty as
                        | "Beginner"
                        | "Intermediate"
                        | "Advanced"
                    )}`}
                  >
                    {currentCard.difficulty}
                  </span>
                  <div className="flex items-center gap-1 text-xs text-muted-foreground">
                    <Clock className="w-3 h-3" />
                    {currentCard.estimatedTime}
                  </div>
                </div>
              </div>

              {/* Question */}
              {cardState === "question" && (
                <div className="space-y-6">
                  <div className="text-center">
                    <div className="text-2xl font-bold leading-relaxed">
                      {currentCard.question}
                    </div>
                  </div>

                  <div className="flex flex-col items-center gap-4 text-muted-foreground">
                    <div className="animate-bounce">
                      <ChevronUp className="w-6 h-6" />
                    </div>
                    <p className="text-sm text-center">
                      Swipe up to reveal answer
                    </p>
                  </div>
                </div>
              )}

              {/* Answer */}
              {cardState === "answer" && (
                <div className="space-y-6">
                  <div className="text-center">
                    <div className="text-lg font-semibold mb-2 text-primary">
                      Answer:
                    </div>
                    <div className="text-xl leading-relaxed mb-4">
                      {currentCard.answer}
                    </div>
                    {currentCard.explanation && (
                      <div className="text-sm text-muted-foreground p-4 bg-muted/50 rounded-lg">
                        💡 {currentCard.explanation}
                      </div>
                    )}
                  </div>

                  <div className="flex flex-col items-center gap-4 text-muted-foreground">
                    <div className="animate-bounce">
                      <ChevronUp className="w-6 h-6" />
                    </div>
                    <p className="text-sm text-center">
                      Swipe up to rate difficulty
                    </p>
                  </div>
                </div>
              )}

              {/* Feedback */}
              {cardState === "feedback" && (
                <div className="space-y-6">
                  <div className="text-center">
                    <div className="text-lg font-semibold mb-4">
                      How was that?
                    </div>
                    <div className="grid grid-cols-3 gap-3">
                      <button
                        onClick={() => handleFeedback("hard")}
                        className="p-4 rounded-xl bg-red-500/10 hover:bg-red-500/20 border border-red-500/20 transition-colors"
                      >
                        <div className="text-2xl mb-2">😓</div>
                        <div className="text-sm font-medium text-red-400">
                          Hard
                        </div>
                      </button>
                      <button
                        onClick={() => handleFeedback("medium")}
                        className="p-4 rounded-xl bg-yellow-500/10 hover:bg-yellow-500/20 border border-yellow-500/20 transition-colors"
                      >
                        <div className="text-2xl mb-2">🤔</div>
                        <div className="text-sm font-medium text-yellow-400">
                          Medium
                        </div>
                      </button>
                      <button
                        onClick={() => handleFeedback("easy")}
                        className="p-4 rounded-xl bg-green-500/10 hover:bg-green-500/20 border border-green-500/20 transition-colors"
                      >
                        <div className="text-2xl mb-2">😊</div>
                        <div className="text-sm font-medium text-green-400">
                          Easy
                        </div>
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Bottom Actions */}
        <div className="px-4 py-4">
          <div className="flex items-center justify-center gap-8 text-sm text-muted-foreground">
            <div className="flex flex-col items-center gap-1">
              <div className="w-8 h-8 rounded-full bg-red-500/20 flex items-center justify-center">
                <span className="text-red-400">←</span>
              </div>
              <span>Learned</span>
            </div>

            <div className="flex flex-col items-center gap-1">
              <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
                <span className="text-primary">↕</span>
              </div>
              <span>Navigate</span>
            </div>

            <div className="flex flex-col items-center gap-1">
              <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center">
                <span className="text-blue-400">→</span>
              </div>
              <span>Save</span>
            </div>
          </div>
        </div>
      </div>

      {/* Card Counter */}
      <div className="fixed bottom-6 left-1/2 transform -translate-x-1/2 bg-card/80 backdrop-blur-sm rounded-full px-4 py-2 border border-border">
        <span className="text-sm font-medium">
          {currentCardIndex + 1} / {learningCards.length}
        </span>
      </div>
    </div>
  );
};

export default LearningApp;
