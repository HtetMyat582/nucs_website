# NUCS_WEBSITE

## Description
NUCS_EDU is a web application built using Django. It provides various features and functionalities for managing educational content and user interactions.

## Features
- Home, About, Contact, and Privacy pages
- User registration, login, and logout
- Program and course listing and detail views
- Faculty listing and detail views
- Enrollment for programs and courses
- Search functionality (single keyword)
- News and events display
- Responsive design and theme toggle
- Student and faculty portals (basic structure)
- Admin interface (default Django)

## Known Bugs & Missing Features
- The copyright year ({{ now }}) does not appear on some pages because now() is not passed in all views.
- Search only works for single-word queries; multi-word (space-separated) queries return no results.
- Search results page does not provide links to detail pages (missing <a> tags).
- In mobile view, navbar buttons are left-aligned under the logo when toggled, which is not the intended design.
- Footer links are left-aligned on mobile; only logo, text, and social icons are centered.
- Events and calendar are not linked; events do not appear on the calendar.
- Faculty and student portals lack class management and data chart features.
- The Django admin page is not customized or styled.
