-- Bulk-imported participants with no UserProfile had their spreadsheet's
-- Country column parsed but discarded, leaving the admin participants list
-- blank for anyone without a pre-existing profile. Add a badge_country
-- fallback field, mirroring badge_prefix/badge_position/badge_organisation.
ALTER TABLE registration ADD COLUMN badge_country VARCHAR(100) NULL;
