-- Add DJCC/local secretariat support-staff badge categories to participation_role
-- (Local Secretariat, Usher, Driver, Medical Staff) — bulk-uploaded via the new
-- names-only import for people with no email on file.
ALTER TABLE registration MODIFY COLUMN participation_role
  ENUM('secretariat','delegate','presenter','speaker','sponsor','moderator',
       'participant','student','exhibitor','world','other_africa','member_state',
       'moh','djcc','local_secretariat','usher','driver','medical_staff') NOT NULL;
