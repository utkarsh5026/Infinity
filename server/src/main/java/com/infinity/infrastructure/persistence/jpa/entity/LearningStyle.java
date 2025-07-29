package com.infinity.infrastructure.persistence.jpa.entity;

public enum LearningStyle {
    VISUAL("Visual"),
    AUDITORY("Auditory"),
    KINESTHETIC("Kinesthetic"),
    READING_WRITING("Reading/Writing"),
    MIXED("Mixed");

    private final String displayName;

    LearningStyle(String displayName) {
        this.displayName = displayName;
    }

    public String getDisplayName() {
        return displayName;
    }
}