"use client";
import React, { useState, useRef } from "react";
import {
  Clock,
  Brain,
  BookOpen,
  Heart,
  Share2,
  MoreHorizontal,
  ChevronDown,
  ChevronUp,
  Lightbulb,
  Code,
  CheckCircle,
  XCircle,
  RotateCcw,
  Bookmark,
  Volume2,
  Eye,
  EyeOff,
  Zap,
  Star,
  Copy,
  Check,
} from "lucide-react";
import ReactMarkdown from "react-markdown";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface LearningCardProps {
  card: any;
  onSwipe: (direction: string) => void;
  onComplete: (card: any) => void;
}

export const LearningCard = ({
  card,
  onSwipe,
  onComplete,
}: LearningCardProps) => {
  const [currentView, setCurrentView] = useState("question"); // question, answer, explanation
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [isLiked, setIsLiked] = useState(false);
  const [copiedCode, setCopiedCode] = useState(false);

  // Touch gesture state
  const [touchStart, setTouchStart] = useState({ x: 0, y: 0 });
  const [touchCurrent, setTouchCurrent] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });

  const cardRef = useRef(null);

  const handleTouchStart = (e) => {
    const touch = e.touches[0];
    setTouchStart({ x: touch.clientX, y: touch.clientY });
    setTouchCurrent({ x: touch.clientX, y: touch.clientY });
    setIsDragging(true);
  };

  const handleTouchMove = (e) => {
    if (!isDragging) return;

    const touch = e.touches[0];
    const deltaX = touch.clientX - touchStart.x;
    const deltaY = touch.clientY - touchStart.y;

    setTouchCurrent({ x: touch.clientX, y: touch.clientY });
    setDragOffset({ x: deltaX, y: deltaY });
  };

  const handleTouchEnd = () => {
    if (!isDragging) return;

    const deltaX = touchCurrent.x - touchStart.x;
    const deltaY = touchCurrent.y - touchStart.y;
    const threshold = 100;

    // Determine swipe direction
    if (Math.abs(deltaX) > Math.abs(deltaY)) {
      // Horizontal swipe
      if (Math.abs(deltaX) > threshold) {
        if (deltaX > 0) {
          onSwipe?.("right"); // Like/Save
          setIsLiked(true);
        } else {
          onSwipe?.("left"); // Skip
        }
      }
    } else {
      // Vertical swipe
      if (Math.abs(deltaY) > threshold) {
        if (deltaY > 0) {
          onSwipe?.("down"); // Previous
        } else {
          onSwipe?.("up"); // Next
        }
      }
    }

    // Reset state
    setIsDragging(false);
    setDragOffset({ x: 0, y: 0 });
  };

  const handleCardTap = () => {
    if (currentView === "question") {
      setCurrentView("answer");
    } else if (currentView === "answer") {
      setCurrentView("explanation");
    } else {
      setCurrentView("question");
    }
  };

  const copyCodeToClipboard = () => {
    const codeBlocks = cardRef.current?.querySelectorAll("code");
    if (codeBlocks && codeBlocks.length > 0) {
      const codeText = Array.from(codeBlocks)
        .map((block) => block.textContent)
        .join("\n\n");

      navigator.clipboard?.writeText(codeText);
      setCopiedCode(true);
      setTimeout(() => setCopiedCode(false), 2000);
    }
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty.toLowerCase()) {
      case "beginner":
        return "bg-[color:--learning-success] text-card-foreground border-[color:--learning-success]";
      case "intermediate":
        return "bg-[color:--learning-warning] text-card-foreground border-[color:--learning-warning]";
      case "advanced":
        return "bg-[color:--learning-error] text-card-foreground border-[color:--learning-error]";
      default:
        return "bg-muted text-muted-foreground border-muted";
    }
  };

  const getViewIcon = () => {
    switch (currentView) {
      case "question":
        return <Brain className="w-4 h-4" />;
      case "answer":
        return <CheckCircle className="w-4 h-4" />;
      case "explanation":
        return <Lightbulb className="w-4 h-4" />;
      default:
        return <BookOpen className="w-4 h-4" />;
    }
  };

  const transform = isDragging
    ? `translate(${dragOffset.x * 0.1}px, ${dragOffset.y * 0.1}px) scale(0.98)`
    : "translate(0px, 0px) scale(1)";

  return (
    <div className="relative w-full max-w-md mx-auto">
      {/* Swipe Indicators */}
      <div
        className={cn(
          "absolute -left-16 top-1/2 transform -translate-y-1/2 transition-opacity duration-200",
          dragOffset.x > 50 ? "opacity-100" : "opacity-0"
        )}
      >
        <div className="bg-[color:--learning-success] text-primary-foreground p-3 rounded-full shadow-lg">
          <Heart className="w-6 h-6" />
        </div>
      </div>

      <div
        className={cn(
          "absolute -right-16 top-1/2 transform -translate-y-1/2 transition-opacity duration-200",
          dragOffset.x < -50 ? "opacity-100" : "opacity-0"
        )}
      >
        <div className="bg-[color:--learning-error] text-primary-foreground p-3 rounded-full shadow-lg">
          <XCircle className="w-6 h-6" />
        </div>
      </div>

      {/* Main Card */}
      <div
        ref={cardRef}
        className="bg-card rounded-3xl shadow-xl border border-border overflow-hidden transition-all duration-200 ease-out"
        style={{ transform }}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-muted/50 to-accent/10 px-6 py-4 border-b border-border">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center space-x-2">
              <span className="bg-card px-3 py-1 rounded-full text-sm font-medium text-card-foreground shadow-sm border border-border">
                {card.category}
              </span>
              <span
                className={cn(
                  "px-3 py-1 rounded-full text-xs font-medium border",
                  getDifficultyColor(card.difficulty)
                )}
              >
                {card.difficulty}
              </span>
            </div>
            <div className="flex items-center space-x-2 text-muted-foreground">
              <Clock className="w-4 h-4" />
              <span className="text-sm">{card.timeToRead}</span>
            </div>
          </div>

          <h2 className="text-xl font-bold text-card-foreground mb-2">
            {card.topic}
          </h2>

          {/* Progress Indicator */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              {getViewIcon()}
              <span className="text-sm font-medium text-muted-foreground capitalize">
                {currentView}
              </span>
            </div>
            <div className="flex space-x-1">
              <div
                className={cn(
                  "w-2 h-2 rounded-full",
                  currentView === "question"
                    ? "bg-[color:--learning-progress]"
                    : "bg-muted"
                )}
              />
              <div
                className={cn(
                  "w-2 h-2 rounded-full",
                  currentView === "answer"
                    ? "bg-[color:--learning-progress]"
                    : "bg-muted"
                )}
              />
              <div
                className={cn(
                  "w-2 h-2 rounded-full",
                  currentView === "explanation"
                    ? "bg-[color:--learning-progress]"
                    : "bg-muted"
                )}
              />
            </div>
          </div>
        </div>

        {/* Content Area */}
        <div
          className="px-6 py-6 min-h-[400px] cursor-pointer"
          onClick={handleCardTap}
        >
          <div className="prose prose-sm max-w-none text-card-foreground">
            {currentView === "question" && (
              <ReactMarkdown>{card.question}</ReactMarkdown>
            )}

            {currentView === "answer" && (
              <ReactMarkdown>{card.answer}</ReactMarkdown>
            )}

            {currentView === "explanation" && (
              <ReactMarkdown>{card.explanation}</ReactMarkdown>
            )}
          </div>

          {/* Tap Hint */}
          {currentView !== "explanation" && (
            <div className="mt-6 text-center">
              <div className="inline-flex items-center space-x-2 text-muted-foreground text-sm">
                <span>
                  Tap to{" "}
                  {currentView === "question"
                    ? "reveal answer"
                    : "see explanation"}
                </span>
                {currentView === "question" ? (
                  <ChevronDown className="w-4 h-4" />
                ) : (
                  <Lightbulb className="w-4 h-4" />
                )}
              </div>
            </div>
          )}
        </div>

        {/* Action Bar */}
        <div className="px-6 py-4 bg-muted/30 border-t border-border">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setIsLiked(!isLiked)}
                className={cn(
                  "rounded-full",
                  isLiked &&
                    "bg-[color:--learning-error]/10 text-[color:--learning-error] hover:bg-[color:--learning-error]/20"
                )}
              >
                <Heart className={cn("w-5 h-5", isLiked && "fill-current")} />
              </Button>

              <Button
                variant="ghost"
                size="icon"
                onClick={() => setIsBookmarked(!isBookmarked)}
                className={cn(
                  "rounded-full",
                  isBookmarked &&
                    "bg-[color:--learning-info]/10 text-[color:--learning-info] hover:bg-[color:--learning-info]/20"
                )}
              >
                <Bookmark
                  className={cn("w-5 h-5", isBookmarked && "fill-current")}
                />
              </Button>

              <Button
                variant="ghost"
                size="icon"
                onClick={copyCodeToClipboard}
                className="rounded-full"
              >
                {copiedCode ? (
                  <Check className="w-5 h-5 text-[color:--learning-success]" />
                ) : (
                  <Copy className="w-5 h-5" />
                )}
              </Button>
            </div>

            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-1 text-[color:--learning-warning]">
                <Zap className="w-4 h-4" />
                <span className="text-sm font-bold">+{card.xp} XP</span>
              </div>

              <Button
                onClick={() => onComplete?.(card)}
                className="rounded-full font-medium"
              >
                Complete
              </Button>
            </div>
          </div>

          {/* Tags */}
          <div className="mt-3 flex flex-wrap gap-2">
            {card.tags?.map((tag, index) => (
              <span
                key={index}
                className="bg-secondary text-secondary-foreground px-2 py-1 rounded-full text-xs border border-border"
              >
                #{tag}
              </span>
            ))}
          </div>
        </div>

        {/* Swipe Instructions */}
        <div className="absolute bottom-2 right-2 text-xs text-muted-foreground text-right leading-tight">
          <div>↕ Swipe up/down: Next/Previous</div>
          <div>↔ Swipe left/right: Skip/Like</div>
        </div>
      </div>

      {/* Custom Styles for Markdown */}
      <style jsx>{`
        .markdown-content h1 {
          font-size: 1.5rem;
          font-weight: 700;
          margin-bottom: 1rem;
          color: hsl(var(--card-foreground));
        }

        .markdown-content h2 {
          font-size: 1.25rem;
          font-weight: 600;
          margin-bottom: 0.75rem;
          color: hsl(var(--card-foreground));
        }

        .markdown-content h3 {
          font-size: 1.125rem;
          font-weight: 600;
          margin-bottom: 0.5rem;
          color: hsl(var(--muted-foreground));
        }

        .markdown-content strong {
          font-weight: 600;
          color: hsl(var(--card-foreground));
        }

        .markdown-content em {
          font-style: italic;
          color: hsl(var(--muted-foreground));
        }

        .markdown-content code {
          background-color: hsl(var(--muted));
          color: hsl(var(--learning-error));
          padding: 0.125rem 0.25rem;
          border-radius: 0.25rem;
          font-family: "SF Mono", Monaco, "Cascadia Code", "Roboto Mono",
            Consolas, "Courier New", monospace;
          font-size: 0.875rem;
        }

        .markdown-content pre {
          background-color: hsl(var(--card));
          color: hsl(var(--card-foreground));
          padding: 1rem;
          border-radius: 0.5rem;
          overflow-x: auto;
          margin: 1rem 0;
          border: 1px solid hsl(var(--border));
        }

        .markdown-content pre code {
          background-color: transparent;
          color: inherit;
          padding: 0;
        }

        .markdown-content ul {
          list-style-type: disc;
          margin-left: 1.5rem;
          margin-bottom: 1rem;
        }

        .markdown-content li {
          margin-bottom: 0.5rem;
          line-height: 1.6;
        }
      `}</style>
    </div>
  );
};
