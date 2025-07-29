package com.infinity.infrastructure.persistence.jpa.repository;

import com.infinity.infrastructure.persistence.jpa.entity.UserEntity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface JpaUserRepository extends JpaRepository<UserEntity, UUID> {

    // Basic query methods
    Optional<UserEntity> findByUsername(String username);

    Optional<UserEntity> findByEmail(String email);

    Optional<UserEntity> findByUsernameOrEmail(String username, String email);

    boolean existsByUsername(String username);

    boolean existsByEmail(String email);

    Optional<UserEntity> findByEmailVerificationToken(String token);

    Optional<UserEntity> findByPasswordResetToken(String token);

    // Active users
    List<UserEntity> findByActiveTrue();

    Page<UserEntity> findByActiveTrue(Pageable pageable);

    // Users registered recently
    @Query("SELECT u FROM UserEntity u WHERE u.createdAt >= :since AND u.active = true")
    List<UserEntity> findUsersRegisteredSince(@Param("since") LocalDateTime since);

    // Users who haven't logged in recently
    @Query("SELECT u FROM UserEntity u WHERE u.lastLoginAt < :before OR u.lastLoginAt IS NULL")
    List<UserEntity> findInactiveUsers(@Param("before") LocalDateTime before);

    // Update operations
    @Modifying
    @Query("UPDATE UserEntity u SET u.lastLoginAt = :loginTime WHERE u.id = :userId")
    void updateLastLoginTime(@Param("userId") UUID userId, @Param("loginTime") LocalDateTime loginTime);

    @Modifying
    @Query("UPDATE UserEntity u SET u.emailVerified = true, u.emailVerificationToken = null WHERE u.id = :userId")
    void markEmailAsVerified(@Param("userId") UUID userId);

    @Modifying
    @Query("UPDATE UserEntity u SET u.loginAttempts = :attempts WHERE u.id = :userId")
    void updateLoginAttempts(@Param("userId") UUID userId, @Param("attempts") Integer attempts);

    @Modifying
    @Query("UPDATE UserEntity u SET u.accountLockedUntil = :lockUntil WHERE u.id = :userId")
    void lockAccount(@Param("userId") UUID userId, @Param("lockUntil") LocalDateTime lockUntil);

    // Search users
    @Query("SELECT u FROM UserEntity u WHERE " +
            "(LOWER(u.username) LIKE LOWER(CONCAT('%', :search, '%')) OR " +
            "LOWER(u.email) LIKE LOWER(CONCAT('%', :search, '%')) OR " +
            "LOWER(u.firstName) LIKE LOWER(CONCAT('%', :search, '%')) OR " +
            "LOWER(u.lastName) LIKE LOWER(CONCAT('%', :search, '%'))) AND " +
            "u.active = true")
    Page<UserEntity> searchUsers(@Param("search") String search, Pageable pageable);

    // Count queries
    @Query("SELECT COUNT(u) FROM UserEntity u WHERE u.createdAt >= :since")
    long countUsersRegisteredSince(@Param("since") LocalDateTime since);

    @Query("SELECT COUNT(u) FROM UserEntity u WHERE u.active = true")
    long countActiveUsers();
}