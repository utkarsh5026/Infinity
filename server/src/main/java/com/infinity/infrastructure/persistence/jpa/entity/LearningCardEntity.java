package com.infinity.infrastructure.persistence.jpa.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

@Entity
@Table(name = "learning_cards", indexes = {
        @Index(name = "idx_card_topic_id", columnList = "topic_id"),
        @Index(name = "idx_card_difficulty", columnList = "difficulty_level"),
        @Index(name = "idx_card_type", columnList = "content_type"),
        @Index(name = "idx_card_created_at", columnList = "created_at")
})
public class LearningCardEntity extends BaseAuditableEntity {

    @NotBlank
    @Size(max = 500)
    @Column(name = "question", nullable = false, length = 500)
    private String question;

    @NotBlank
    @Size(max = 2000)
    @Column(name = "answer", nullable = false, length = 2000)
    private String answer;

    @Size(max = 1000)
    @Column(name = "explanation", length = 1000)
    private String explanation;

    @Size(max = 500)
    @Column(name = "hint", length = 500)
    private String hint;

    @Enumerated(EnumType.STRING)
    @Column(name = "content_type", nullable = false, length = 20)
    private ContentType contentType = ContentType.QUESTION_ANSWER;

    @Enumerated(EnumType.STRING)
    @Column(name = "difficulty_level", nullable = false, length = 20)
    private DifficultyLevel difficultyLevel;

    @Column(name = "tags", length = 500)
    private String tags; // JSON array or comma-separated

    @Column(name = "llm_model_used", length = 50)
    private String llmModelUsed;

    @Column(name = "generation_prompt", columnDefinition = "TEXT")
    private String generationPrompt;

    // Relationships
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "topic_id", nullable = false, foreignKey = @ForeignKey(name = "fk_learning_card_topic"))
    private TopicEntity topic;

    // Constructors
    public LearningCardEntity() {
    }

    public LearningCardEntity(String question, String answer, TopicEntity topic,
            DifficultyLevel difficultyLevel) {
        this.question = question;
        this.answer = answer;
        this.topic = topic;
        this.difficultyLevel = difficultyLevel;
    }

    // Getters and Setters
    public String getQuestion() {
        return question;
    }

    public void setQuestion(String question) {
        this.question = question;
    }

    public String getAnswer() {
        return answer;
    }

    public void setAnswer(String answer) {
        this.answer = answer;
    }

    public String getExplanation() {
        return explanation;
    }

    public void setExplanation(String explanation) {
        this.explanation = explanation;
    }

    public String getHint() {
        return hint;
    }

    public void setHint(String hint) {
        this.hint = hint;
    }

    public ContentType getContentType() {
        return contentType;
    }

    public void setContentType(ContentType contentType) {
        this.contentType = contentType;
    }

    public DifficultyLevel getDifficultyLevel() {
        return difficultyLevel;
    }

    public void setDifficultyLevel(DifficultyLevel difficultyLevel) {
        this.difficultyLevel = difficultyLevel;
    }

    public String getTags() {
        return tags;
    }

    public void setTags(String tags) {
        this.tags = tags;
    }

    public String getLlmModelUsed() {
        return llmModelUsed;
    }

    public void setLlmModelUsed(String llmModelUsed) {
        this.llmModelUsed = llmModelUsed;
    }

    public String getGenerationPrompt() {
        return generationPrompt;
    }

    public void setGenerationPrompt(String generationPrompt) {
        this.generationPrompt = generationPrompt;
    }

    public TopicEntity getTopic() {
        return topic;
    }

    public void setTopic(TopicEntity topic) {
        this.topic = topic;
    }
}