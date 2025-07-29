package com.infinity.infrastructure.persistence.jpa.repository;

import com.infinity.infrastructure.persistence.jpa.entity.DifficultyLevel;
import com.infinity.infrastructure.persistence.jpa.entity.TopicEntity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface JpaTopicRepository extends JpaRepository<TopicEntity, UUID> {

    // Find by basic properties
    Optional<TopicEntity> findByNameAndActiveTrue(String name);

    List<TopicEntity> findByCategoryAndActiveTrue(String category);

    List<TopicEntity> findByDifficultyLevelAndActiveTrue(DifficultyLevel difficultyLevel);

    List<TopicEntity> findByCategoryAndDifficultyLevelAndActiveTrue(String category, DifficultyLevel difficultyLevel);

    // Paginated queries
    Page<TopicEntity> findByActiveTrue(Pageable pageable);

    Page<TopicEntity> findByCategoryAndActiveTrue(String category, Pageable pageable);

    Page<TopicEntity> findByDifficultyLevelAndActiveTrue(DifficultyLevel difficultyLevel, Pageable pageable);

    // Topics with minimum card count
    @Query("SELECT t FROM TopicEntity t WHERE t.totalCardsCount >= :minCards AND t.active = true")
    List<TopicEntity> findTopicsWithMinimumCards(@Param("minCards") Integer minCards);

    // Search topics
    @Query("SELECT t FROM TopicEntity t WHERE " +
            "(LOWER(t.name) LIKE LOWER(CONCAT('%', :search, '%')) OR " +
            "LOWER(t.description) LIKE LOWER(CONCAT('%', :search, '%')) OR " +
            "LOWER(t.tags) LIKE LOWER(CONCAT('%', :search, '%'))) AND " +
            "t.active = true")
    Page<TopicEntity> searchTopics(@Param("search") String search, Pageable pageable);

    // Categories
    @Query("SELECT DISTINCT t.category FROM TopicEntity t WHERE t.active = true ORDER BY t.category")
    List<String> findAllCategories();

    // Update operations
    @Modifying
    @Query("UPDATE TopicEntity t SET t.totalCardsCount = t.totalCardsCount + 1 WHERE t.id = :topicId")
    void incrementCardCount(@Param("topicId") UUID topicId);

    @Modifying
    @Query("UPDATE TopicEntity t SET t.totalCardsCount = GREATEST(0, t.totalCardsCount - 1) WHERE t.id = :topicId")
    void decrementCardCount(@Param("topicId") UUID topicId);

    @Query("SELECT t.category, COUNT(t) FROM TopicEntity t WHERE t.active = true GROUP BY t.category")
    List<Object[]> countTopicsByCategory();
}