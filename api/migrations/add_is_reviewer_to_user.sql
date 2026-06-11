-- Add is_reviewer flag to distinguish reviewer-pool users from regular participants
ALTER TABLE `user` ADD COLUMN `is_reviewer` TINYINT(1) NOT NULL DEFAULT 0;

-- Backfill: mark anyone already assigned as a reviewer in abstract_reviewer
UPDATE `user` SET is_reviewer = 1
WHERE id IN (SELECT DISTINCT reviewer_id FROM abstract_reviewer);
