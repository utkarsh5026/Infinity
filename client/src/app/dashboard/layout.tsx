"use client";

import React, { useState } from "react";
import {
  Clock,
  Trophy,
  Target,
  Brain,
  BookOpen,
  TrendingUp,
  Star,
  ChevronRight,
  Play,
  RotateCcw,
  Heart,
  Share2,
  MoreHorizontal,
  Zap,
  Calendar,
  Award,
} from "lucide-react";

// Mock data for demonstration
const mockLearningCard = {
  id: 1,
  topic: "JavaScript Fundamentals",
  question:
    "What is the difference between 'let', 'const', and 'var' in JavaScript?",
  answer:
    "'let' and 'const' are block-scoped, while 'var' is function-scoped. 'const' cannot be reassigned after declaration, while 'let' and 'var' can be.",
  difficulty: "Beginner",
  timeToRead: "2 min",
  category: "Programming",
};

const mockTopics = [
  { name: "JavaScript", progress: 75, icon: "💻", color: "bg-yellow-500" },
  { name: "React", progress: 60, icon: "⚛️", color: "bg-blue-500" },
  { name: "Python", progress: 40, icon: "🐍", color: "bg-green-500" },
  { name: "Data Science", progress: 25, icon: "📊", color: "bg-purple-500" },
];

const mockStats = {
  streak: 7,
  totalCards: 124,
  todayGoal: 10,
  completed: 6,
  weeklyXP: 850,
};

const LearningCard = ({ card, onSwipe }) => {
  const [isFlipped, setIsFlipped] = useState(false);
  const [startY, setStartY] = useState(0);
  const [currentY, setCurrentY] = useState(0);
  const [isDragging, setIsDragging] = useState(false);

  const handleTouchStart = (e) => {
    setStartY(e.touches[0].clientY);
    setIsDragging(true);
  };

  const handleTouchMove = (e) => {
    if (!isDragging) return;
    setCurrentY(e.touches[0].clientY - startY);
  };

  const handleTouchEnd = () => {
    if (Math.abs(currentY) > 100) {
      onSwipe(currentY > 0 ? "down" : "up");
    }
    setCurrentY(0);
    setIsDragging(false);
  };

  return (
    <div
      className={`relative w-full h-[500px] bg-gradient-to-br from-blue-50 to-indigo-100 rounded-2xl shadow-lg transform transition-transform duration-300 ${
        isDragging ? "scale-95" : "scale-100"
      }`}
      style={{ transform: `translateY(${currentY * 0.1}px)` }}
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
      onClick={() => setIsFlipped(!isFlipped)}
    >
      <div className="absolute top-4 left-4 right-4 flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <span className="bg-white/80 backdrop-blur-sm px-3 py-1 rounded-full text-sm font-medium text-gray-700">
            {card.category}
          </span>
          <span className="bg-green-500/80 text-white px-2 py-1 rounded-full text-xs font-medium">
            {card.difficulty}
          </span>
        </div>
        <div className="flex items-center space-x-2">
          <Clock className="w-4 h-4 text-gray-600" />
          <span className="text-sm text-gray-600">{card.timeToRead}</span>
        </div>
      </div>

      <div className="absolute inset-0 p-6 pt-16 flex flex-col justify-center">
        <div
          className={`transition-opacity duration-300 ${
            isFlipped ? "opacity-0" : "opacity-100"
          }`}
        >
          <h2 className="text-xl font-bold text-gray-800 mb-4">{card.topic}</h2>
          <p className="text-lg text-gray-700 leading-relaxed">
            {card.question}
          </p>
          <div className="mt-8 text-center">
            <p className="text-sm text-gray-500">Tap to reveal answer</p>
          </div>
        </div>

        <div
          className={`absolute inset-6 pt-10 transition-opacity duration-300 ${
            isFlipped ? "opacity-100" : "opacity-0"
          }`}
        >
          <div className="bg-white/80 backdrop-blur-sm rounded-xl p-4 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-3">
              Answer:
            </h3>
            <p className="text-gray-700 leading-relaxed">{card.answer}</p>
          </div>
        </div>
      </div>

      <div className="absolute bottom-4 left-4 right-4 flex justify-between items-center">
        <div className="flex space-x-4">
          <button className="bg-white/80 backdrop-blur-sm p-3 rounded-full shadow-sm hover:bg-white transition-colors">
            <RotateCcw className="w-5 h-5 text-gray-600" />
          </button>
          <button className="bg-white/80 backdrop-blur-sm p-3 rounded-full shadow-sm hover:bg-white transition-colors">
            <Heart className="w-5 h-5 text-red-500" />
          </button>
          <button className="bg-white/80 backdrop-blur-sm p-3 rounded-full shadow-sm hover:bg-white transition-colors">
            <Share2 className="w-5 h-5 text-gray-600" />
          </button>
        </div>
        <button className="bg-white/80 backdrop-blur-sm p-3 rounded-full shadow-sm hover:bg-white transition-colors">
          <MoreHorizontal className="w-5 h-5 text-gray-600" />
        </button>
      </div>

      <div className="absolute right-4 top-1/2 transform -translate-y-1/2 text-xs text-gray-400 writing-mode-vertical">
        Swipe up for next • Swipe down to review
      </div>
    </div>
  );
};

const ProgressRing = ({ progress, size = 60 }) => {
  const radius = (size - 8) / 2;
  const circumference = radius * 2 * Math.PI;
  const strokeDasharray = circumference;
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  return (
    <div className="relative inline-flex">
      <svg width={size} height={size} className="transform -rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="currentColor"
          strokeWidth="4"
          fill="transparent"
          className="text-gray-200"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="currentColor"
          strokeWidth="4"
          fill="transparent"
          strokeDasharray={strokeDasharray}
          strokeDashoffset={strokeDashoffset}
          className="text-blue-500 transition-all duration-300"
          strokeLinecap="round"
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-sm font-bold text-gray-700">{progress}%</span>
      </div>
    </div>
  );
};

const Dashboard = () => {
  const [currentCard, setCurrentCard] = useState(mockLearningCard);

  const handleSwipe = (direction) => {
    console.log(`Swiped ${direction}`);
    // Here you would implement the logic to load the next card
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-md mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold text-gray-900">
                Good morning! 👋
              </h1>
              <p className="text-sm text-gray-600">
                Ready to learn something new?
              </p>
            </div>
            <div className="flex items-center space-x-2">
              <div className="flex items-center space-x-1 bg-orange-100 px-3 py-1 rounded-full">
                <Zap className="w-4 h-4 text-orange-500" />
                <span className="text-sm font-bold text-orange-700">
                  {mockStats.streak}
                </span>
              </div>
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-sm">JD</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-md mx-auto px-4 pb-20">
        {/* Daily Progress */}
        <div className="mt-6 bg-white rounded-2xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">
              Today's Progress
            </h2>
            <Calendar className="w-5 h-5 text-gray-400" />
          </div>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <ProgressRing
                progress={(mockStats.completed / mockStats.todayGoal) * 100}
              />
              <div>
                <p className="text-2xl font-bold text-gray-900">
                  {mockStats.completed}/{mockStats.todayGoal}
                </p>
                <p className="text-sm text-gray-600">Cards completed</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-lg font-bold text-blue-600">
                {mockStats.weeklyXP} XP
              </p>
              <p className="text-xs text-gray-500">This week</p>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-6 grid grid-cols-2 gap-4">
          <button className="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-4 rounded-xl shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center space-x-2">
              <Play className="w-5 h-5" />
              <span className="font-medium">Continue Learning</span>
            </div>
          </button>
          <button className="bg-white border-2 border-gray-200 text-gray-700 p-4 rounded-xl shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center space-x-2">
              <Target className="w-5 h-5" />
              <span className="font-medium">Set Goals</span>
            </div>
          </button>
        </div>

        {/* Main Learning Card */}
        <div className="mt-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">
              Featured Content
            </h2>
            <button className="text-blue-600 text-sm font-medium">
              View All
            </button>
          </div>
          <LearningCard card={currentCard} onSwipe={handleSwipe} />
        </div>

        {/* Topics Progress */}
        <div className="mt-6 bg-white rounded-2xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Your Topics</h2>
            <ChevronRight className="w-5 h-5 text-gray-400" />
          </div>
          <div className="space-y-4">
            {mockTopics.map((topic, index) => (
              <div key={index} className="flex items-center space-x-4">
                <div
                  className={`w-10 h-10 ${topic.color} rounded-lg flex items-center justify-center text-white font-bold`}
                >
                  {topic.icon}
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <h3 className="font-medium text-gray-900">{topic.name}</h3>
                    <span className="text-sm text-gray-500">
                      {topic.progress}%
                    </span>
                  </div>
                  <div className="mt-1 bg-gray-200 rounded-full h-2">
                    <div
                      className={`${topic.color} h-2 rounded-full transition-all duration-300`}
                      style={{ width: `${topic.progress}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Achievements */}
        <div className="mt-6 bg-gradient-to-r from-purple-50 to-pink-50 rounded-2xl p-6">
          <div className="flex items-center space-x-2 mb-4">
            <Award className="w-5 h-5 text-purple-600" />
            <h2 className="text-lg font-semibold text-gray-900">
              Recent Achievement
            </h2>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center">
              <Trophy className="w-6 h-6 text-white" />
            </div>
            <div>
              <h3 className="font-medium text-gray-900">Week Warrior</h3>
              <p className="text-sm text-gray-600">
                Completed 7 days in a row!
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Navigation */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200">
        <div className="max-w-md mx-auto px-4">
          <div className="flex items-center justify-around py-2">
            <button className="flex flex-col items-center py-2 px-4">
              <BookOpen className="w-6 h-6 text-blue-600" />
              <span className="text-xs text-blue-600 mt-1">Learn</span>
            </button>
            <button className="flex flex-col items-center py-2 px-4">
              <Brain className="w-6 h-6 text-gray-400" />
              <span className="text-xs text-gray-400 mt-1">Topics</span>
            </button>
            <button className="flex flex-col items-center py-2 px-4">
              <TrendingUp className="w-6 h-6 text-gray-400" />
              <span className="text-xs text-gray-400 mt-1">Progress</span>
            </button>
            <button className="flex flex-col items-center py-2 px-4">
              <Star className="w-6 h-6 text-gray-400" />
              <span className="text-xs text-gray-400 mt-1">Profile</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
