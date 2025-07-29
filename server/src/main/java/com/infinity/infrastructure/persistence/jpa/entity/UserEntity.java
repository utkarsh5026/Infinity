package com.infinity.infrastructure.persistence.jpa.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "users", indexes = {
        @Index(name = "idx_user_email", columnList = "email", unique = true),
        @Index(name = "idx_user_username", columnList = "username", unique = true),
        @Index(name = "idx_user_active", columnList = "active"),
        @Index(name = "idx_user_created_at", columnList = "created_at")
})
public class UserEntity extends BaseAuditableEntity {

    @NotBlank
    @Size(min = 3, max = 50)
    @Column(name = "username", nullable = false, unique = true, length = 50)
    private String username;

    @NotBlank
    @Email
    @Size(max = 100)
    @Column(name = "email", nullable = false, unique = true, length = 100)
    private String email;

    @NotBlank
    @Size(min = 60, max = 60) // BCrypt hash length
    @Column(name = "password_hash", nullable = false, length = 60)
    private String passwordHash;

    @Size(max = 100)
    @Column(name = "first_name", length = 100)
    private String firstName;

    @Size(max = 100)
    @Column(name = "last_name", length = 100)
    private String lastName;

    @Embedded
    private UserPreferencesEmbeddable preferences;

    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(name = "user_favorite_topics", joinColumns = @JoinColumn(name = "user_id"), inverseJoinColumns = @JoinColumn(name = "topic_id"), indexes = {
            @Index(name = "idx_favorite_user_id", columnList = "user_id"),
            @Index(name = "idx_favorite_topic_id", columnList = "topic_id")
    })
    private Set<TopicEntity> favoriteTopics = new HashSet<>();

    // Constructors
    public UserEntity() {
    }

    public UserEntity(String username, String email, String passwordHash) {
        this.username = username;
        this.email = email;
        this.passwordHash = passwordHash;
    }

    public String getFullName() {
        if (firstName != null && lastName != null) {
            return firstName + " " + lastName;
        } else if (firstName != null) {
            return firstName;
        } else if (lastName != null) {
            return lastName;
        }
        return username;
    }

    // Getters and Setters
    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPasswordHash() {
        return passwordHash;
    }

    public void setPasswordHash(String passwordHash) {
        this.passwordHash = passwordHash;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public UserPreferencesEmbeddable getPreferences() {
        return preferences;
    }

    public void setPreferences(UserPreferencesEmbeddable preferences) {
        this.preferences = preferences;
    }

    public Set<TopicEntity> getFavoriteTopics() {
        return favoriteTopics;
    }

    public void setFavoriteTopics(Set<TopicEntity> favoriteTopics) {
        this.favoriteTopics = favoriteTopics;
    }
}