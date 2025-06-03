Changelog
=========

Version 1.0.1 - 2025-06-02
--------------------------

### Added
- Implemented PostgreSQL database integration for storing email tracking data.
- Added function `save_email_tracking_to_db` to insert tracking information into the `email_tracking` table.
- Enabled email tracking with 1x1 pixel for open detection, updating PostgreSQL database when emails are opened.

### Changed
- Removed CSV-based tracking and replaced it with database-based tracking for better data management.
- Refactored email sending logic to handle database inserts correctly.
- Updated exception handling in email sending to log failed attempts.

### Fixed
- Addressed issues with email not sending due to commented-out code, re-enabling the sending process.