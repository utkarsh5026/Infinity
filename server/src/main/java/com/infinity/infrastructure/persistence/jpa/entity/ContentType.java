package com.infinity.infrastructure.persistence.jpa.entity;

public enum ContentType {
    QUESTION_ANSWER("Question & Answer"),
    MULTIPLE_CHOICE("Multiple Choice"),
    TRUE_FALSE("True/False"),
    FILL_IN_BLANK("Fill in the Blank"),
    MATCHING("Matching"),
    EXPLANATION("Explanation"),
    EXAMPLE("Example"),
    DEFINITION("Definition"),
    SCENARIO("Scenario"),
    CALCULATION("Calculation");

    private final String displayName;

    ContentType(String displayName) {
        this.displayName = displayName;
    }

    public String getDisplayName() {
        return displayName;
    }
}