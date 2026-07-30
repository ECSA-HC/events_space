-- Tracks when a participant's badge was last included in a bulk badge PDF
-- export, so the "Choose Names" picker can flag/skip people already
-- exported today instead of silently re-including them.
ALTER TABLE registration ADD COLUMN badge_exported_at TIMESTAMP NULL;
