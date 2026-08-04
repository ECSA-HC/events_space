ALTER TABLE registration MODIFY COLUMN participation_role
  ENUM('secretariat','delegate','presenter','speaker','sponsor','moderator','participant','student','exhibitor','world','other_africa','member_state','moh','djcc','local_secretariat','usher','driver','medical_staff','media') NOT NULL;
