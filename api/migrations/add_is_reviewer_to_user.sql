-- Add is_reviewer flag to distinguish reviewer-pool users from regular participants
ALTER TABLE `user` ADD COLUMN `is_reviewer` TINYINT(1) NOT NULL DEFAULT 0;
