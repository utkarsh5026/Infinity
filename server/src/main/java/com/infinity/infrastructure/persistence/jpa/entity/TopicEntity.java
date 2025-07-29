package com.infinity.infrastructure.persistence.jpa.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "topics", indexes = {
        @Index(name = "idx_topic_name", columnList = "name"),
        @Index(name = "idx_topic_category", columnList = "category"),
        @Index(name = "idx_topic_difficulty", columnList = "difficulty_level"),
        @Index(name = "idx_topic_active", columnList = "active")
})
public class TopicEntity extends BaseAuditableEntity {

    @NotBlank
    @Size(max = 100)
    @Column(name = "name", nullable = false, length = 100)
    private String name;

    @Size(max = 500)
    @Column(name = "description", length = 500)
    private String description;

    @NotBlank
    @Size(max = 50)
    @Column(name = "category", nullable = false, length = 50)
    private String category;

    @Enumerated(EnumType.STRING)
    @Column(name = "difficulty_level", nullable = false, length = 20)
    private DifficultyLevel difficultyLevel = DifficultyLevel.BEGINNER;

    @Column(name = "total_cards_count", nullable = false)
    private Integer totalCardsCount = 0;

    @Column(name = "tags", length = 500)
    private String tags; // Comma-separated tags

    @Column(name = "prerequisites", length = 500)
    private String prerequisites; // JSON or comma-separated prerequisite topic IDs

    // Relationships
    @OneToMany(mappedBy = "topic", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private Set<LearningCardEntity> learningCards = new HashSet<>();

    @ManyToMany(mappedBy = "favoriteTopics", fetch = FetchType.LAZY)
    private Set<UserEntity> favoredByUsers = new HashSet<>();

    // Constructors
    public TopicEntity() {
    }

    public TopicEntity(String name, String category, DifficultyLevel difficultyLevel) {
        this.name = name;
        this.category = category;
        this.difficultyLevel = difficultyLevel;
    }

    // Business methods
    public void incrementCardsCount() {
        this.totalCardsCount = (this.totalCardsCount == null) ? 1 : this.totalCardsCount + 1;
    }

    public void decrementCardsCount() {
        if (this.totalCardsCount != null && this.totalCardsCount > 0) {
            this.totalCardsCount--;
        }
    }

    // Getters and Setters
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public DifficultyLevel getDifficultyLevel() {
        return difficultyLevel;
    }

    public void setDifficultyLevel(DifficultyLevel difficultyLevel) {
        this.difficultyLevel = difficultyLevel;
    }

    public Integer getTotalCardsCount() {
        return totalCardsCount;
    }

    public void setTotalCardsCount(Integer totalCardsCount) {
        this.totalCardsCount = totalCardsCount;
    }

    public String getTags() {
        return tags;
    }

    public void setTags(String tags) {
        this.tags = tags;
    }

    public String getPrerequisites() {
        return prerequisites;
    }

    public void setPrerequisites(String prerequisites) {
        this.prerequisites = prerequisites;
    }

    public Set<LearningCardEntity> getLearningCards() {
        return learningCards;
    }

    public void setLearningCards(Set<LearningCardEntity> learningCards) {
        this.learningCards = learningCards;
    }

    public Set<UserEntity> getFavoredByUsers() {
        return favoredByUsers;
    }

    public void setFavoredByUsers(Set<UserEntity> favoredByUsers) {
        this.favoredByUsers = favoredByUsers;
    }
}