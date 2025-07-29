package com.infinity.infrastructure.persistence.jpa.entity;

public enum DifficultyLevel {
    BEGINNER(1, "Beginner"),
    INTERMEDIATE(2, "Intermediate"),
    ADVANCED(3, "Advanced"),
    EXPERT(4, "Expert");

    private final int level;
    private final String displayName;

    DifficultyLevel(int level, String displayName) {
        this.level = level;
        this.displayName = displayName;
    }

    public int getLevel() {
        return level;
    }

    public String getDisplayName() {
        return displayName;
    }

    public boolean isHigherThan(DifficultyLevel other) {
        return this.level > other.level;
    }

    public boolean isLowerThan(DifficultyLevel other) {
        return this.level < other.level;
    }
}