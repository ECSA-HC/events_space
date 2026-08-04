// Shared participation-role options for admin dropdowns (Add Participant,
// Import Participants, Edit Role, Import Names Only) — single source of
// truth instead of copy-pasting this list in every modal. Must match the
// Python ParticipationRole enum in api/models/models.py and the friendly
// _ROLE_LABELS dict in api/routers/events.py.
export const PARTICIPATION_ROLES = [
  { value: 'secretariat',       label: 'ECSA-HC Secretariat' },
  { value: 'djcc',              label: 'DJCC Member' },
  { value: 'moh',               label: 'Country Delegate (Ministry of Health)' },
  { value: 'member_state',      label: 'Participant – ECSA Member State' },
  { value: 'other_africa',      label: 'Participant – Other African Country' },
  { value: 'world',             label: 'International Participant' },
  { value: 'delegate',          label: 'Delegate' },
  { value: 'presenter',         label: 'Presenter' },
  { value: 'speaker',           label: 'Speaker' },
  { value: 'moderator',         label: 'Moderator' },
  { value: 'participant',       label: 'General Participant' },
  { value: 'student',           label: 'Student' },
  { value: 'exhibitor',         label: 'Sponsor / Exhibitor' },
  { value: 'sponsor',           label: 'Sponsor' },
  { value: 'local_secretariat', label: 'Local Secretariat' },
  { value: 'usher',             label: 'Usher' },
  { value: 'driver',            label: 'Driver' },
  { value: 'medical_staff',     label: 'Medical Staff' },
  { value: 'media',             label: 'Media' },
]
