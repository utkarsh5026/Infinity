package com.infinity.infrastructure.persistence.jpa.entity;

import jakarta.persistence.*;

@Embeddable
public class UserPreferencesEmbeddable {

    @Enumerated(EnumType.STRING)
    @Column(name = "learning_style", length = 20)
    private LearningStyle learningStyle = LearningStyle.MIXED;

    @Enumerated(EnumType.STRING)
    @Column(name = "difficulty_preference", length = 20)
    private DifficultyLevel difficultyPreference = DifficultyLevel.INTERMEDIATE;

    @Column(name = "daily_goal_minutes")
    private Integer dailyGoalMinutes = 15;

    @Column(name = "cards_per_session")
    private Integer cardsPerSession = 10;

    @Column(name = "enable_notifications", nullable = false)
    private Boolean enableNotifications = true;

    @Column(name = "enable_sound", nullable = false)
    private Boolean enableSound = true;

    @Column(name = "enable_haptic_feedback", nullable = false)
    private Boolean enableHapticFeedback = true;

    @Column(name = "preferred_session_time", length = 10)
    private String preferredSessionTime; // "09:00", "18:30", etc.

    @Column(name = "timezone", length = 50)
    private String timezone = "UTC";

    @Column(name = "language_code", length = 5)
    private String languageCode = "en";

    @Column(name = "spaced_repetition_enabled", nullable = false)
    private Boolean spacedRepetitionEnabled = true;

    // Constructors
    public UserPreferencesEmbeddable() {
    }

    // Getters and Setters
    public LearningStyle getLearningStyle() {
        return learningStyle;
    }

    public void setLearningStyle(LearningStyle learningStyle) {
        this.learningStyle = learningStyle;
    }

    public DifficultyLevel getDifficultyPreference() {
        return difficultyPreference;
    }

    public void setDifficultyPreference(DifficultyLevel difficultyPreference) {
        this.difficultyPreference = difficultyPreference;
    }

    public Integer getDailyGoalMinutes() {
        return dailyGoalMinutes;
    }

    public void setDailyGoalMinutes(Integer dailyGoalMinutes) {
        this.dailyGoalMinutes = dailyGoalMinutes;
    }

    public Integer getCardsPerSession() {
        return cardsPerSession;
    }

    public void setCardsPerSession(Integer cardsPerSession) {
        this.cardsPerSession = cardsPerSession;
    }

    public Boolean getEnableNotifications() {
        return enableNotifications;
    }

    public void setEnableNotifications(Boolean enableNotifications) {
        this.enableNotifications = enableNotifications;
    }

    public Boolean getEnableSound() {
        return enableSound;
    }

    public void setEnableSound(Boolean enableSound) {
        this.enableSound = enableSound;
    }

    public Boolean getEnableHapticFeedback() {
        return enableHapticFeedback;
    }

    public void setEnableHapticFeedback(Boolean enableHapticFeedback) {
        this.enableHapticFeedback = enableHapticFeedback;
    }

    public String getPreferredSessionTime() {
        return preferredSessionTime;
    }

    public void setPreferredSessionTime(String preferredSessionTime) {
        this.preferredSessionTime = preferredSessionTime;
    }

    public String getTimezone() {
        return timezone;
    }

    public void setTimezone(String timezone) {
        this.timezone = timezone;
    }

    public String getLanguageCode() {
        return languageCode;
    }

    public void setLanguageCode(String languageCode) {
        this.languageCode = languageCode;
    }

    public Boolean getSpacedRepetitionEnabled() {
        return spacedRepetitionEnabled;
    }

    public void setSpacedRepetitionEnabled(Boolean spacedRepetitionEnabled) {
        this.spacedRepetitionEnabled = spacedRepetitionEnabled;
    }
}