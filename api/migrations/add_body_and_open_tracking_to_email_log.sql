-- Add email body storage and open-tracking columns to email_log
ALTER TABLE `email_log`
    ADD COLUMN `body` LONGTEXT NULL AFTER `error_message`,
    ADD COLUMN `opened_at` TIMESTAMP NULL AFTER `body`,
    ADD COLUMN `opened_count` INT NOT NULL DEFAULT 0 AFTER `opened_at`;
