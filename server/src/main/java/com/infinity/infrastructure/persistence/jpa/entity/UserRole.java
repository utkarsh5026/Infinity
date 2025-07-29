package com.infinity.infrastructure.persistence.jpa.entity;

public enum UserRole {
    USER("User"),
    PREMIUM_USER("Premium User"),
    MODERATOR("Moderator"),
    ADMIN("Administrator"),
    SUPER_ADMIN("Super Administrator");

    private final String displayName;

    UserRole(String displayName) {
        this.displayName = displayName;
    }

    public String getDisplayName() {
        return displayName;
    }

    public boolean hasModeratorPrivileges() {
        return this == MODERATOR || this == ADMIN || this == SUPER_ADMIN;
    }

    public boolean hasAdminPrivileges() {
        return this == ADMIN || this == SUPER_ADMIN;
    }
}