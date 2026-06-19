# Changelog

All changes will be documented here.

## Phase 1 - Project Setup

### Completed

- Created the project structure
- Implemented Flask application factory
- Added configuration system
- Created Blueprints
- Registered Blueprints
- Added placeholder routes
- Verified application runs

## Phase 2 - Authentication System

### Completed
- Created User model
- Added database integration
- Created registration form
- Implemented user registration
- Added password hashing
- Prevented duplicate usernames and emails
- Created login form
- Implemented login functionality with sessions
- Added logout functionality
- Created protected dashboard route
- Added flash messages for authentication flow
- Implemented navigation state based on login status

## Phase 3 - Request Management System 

### Completed
- Added Request model
- Implemented User-Request relationship
- Added request creation functionality
- Added My Requests page
- Added Request Details page
- Implemented ownership validation
- Updated navigation for request management

## Phase 4 - Dashboard and Request Overview System

### Completed
- Added dashboard statistics
- Added recent requests section
- Added quick action links
- Added personalized dashboard greeting
- Added empty state handling
- Improved dashboard user experience
- Verified dashboard functionality

## Phase 5 - Role Management and Authorization System

### Completed
- Added role field to User model with default value of User
- Assigned default role on registration
- Stored role in session on login
- Displayed role on dashboard
- Created protected Admin route (Admin only)
- Created protected Engineer route (Engineer only)
- Added access denied flash message and redirect for unauthorized access
- Added role-aware navigation (Admin and Engineer links shown based on role)
- Created admin page template
- Created engineer page template
- Verified all three roles behave differently

## Phase 6 - Role Management System

### Completed
- Created login_required decorator to protect routes from unauthenticated access
- Created role_required decorator to restrict routes by user role
- Applied login_required to all authenticated routes (dashboard, requests)
- Applied role_required to admin and engineer routes
- Removed repeated session checks from individual routes (replaced by decorators)
- Admin page now displays all requests and all users in the system
- Engineer page now displays all approved requests
- Verified all three roles behave correctly with the new decorator system

## Phase 7 - Admin Panel System

### Completed
- Created dedicated Admin Dashboard route and template
- Added system overview statistics (total users, total requests)
- Added recent users and recent requests sections to admin dashboard
- Created admin user list page showing all users with roles
- Created admin request list page showing all requests from all users
- Created admin request detail page
- Protected all admin routes with role_required decorator
- Updated navigation to link to new admin dashboard
- Moved flash messages to base.html for consistent display across all pages

## Phase 8 - Status Tracking Workflow System

### Completed
- Defined allowed statuses: Pending, In Progress, Approved, Rejected
- Added status update route for Admin
- Added status update route for Engineer
- Added status dropdown form to admin request detail page
- Created engineer request detail page with status dropdown form
- Updated engineer page to link to individual request details
- Protected all status update routes with role_required decorator
- Added server-side validation to reject invalid status values
- Status remains visible to regular users on request list and detail pages

## Phase 9 - Status History & Audit Logs System

### Completed
- Created StatusHistory model to record all status changes
- Added relationship between Request and StatusHistory
- Audit log automatically created on every status update
- Stored previous status, new status, changed by username, and timestamp
- Added same-status check to prevent duplicate audit entries
- Status history displayed on admin request detail page
- Status history displayed on engineer request detail page
- History entries ordered by most recent first
- Regular users cannot access audit history
- New database table created automatically on app startup

## Phase 10 - Hardening and UI/UX Enhancement

### Fixes
- Added missing Completed status to ALLOWED_STATUSES and VALID_TRANSITIONS
- Fixed home page to a real landing page instead of a placeholder string
- Fixed dashboard to show all five status counts (Total, Pending, Approved, In Progress, Completed)
- Fixed template structure — organized all templates into blueprint subfolders
- Resolved route conflicts and import errors across auth and admin blueprints
- Fixed CSRF token availability across all forms via global CSRFProtect initialization

### Enhancements
- Added request_type field with dropdown across creation, detail, and all role views
- Added status transition validation per role (Manager, Engineer, Support, Admin)
- Added Profile and Change Password pages
- Added secure first-Admin registration via environment-set registration code
- Added instant role propagation via database-synced session decorator (no logout required)
- Added Manager, Support, and Viewer roles alongside existing User, Engineer, Admin
- Added README.md and requirements.txt for setup and portfolio documentation
- Moved SECRET_KEY and ADMIN_REGISTRATION_CODE to environment variables

### User Interface & Experience
- Implemented enterprise-inspired design system (dark sidebar shell, light content area)
- Added consistent status badge component used across dashboard, tables, and detail pages
- Added monospaced request ID convention (REQ-0042 format) across all request views
- Restyled all tables with consistent headers, spacing, hover states, and horizontal scroll on small screens
- Restyled all forms (login, register, create request, change password, status updates) with consistent fields and focus states
- Added stat tile component with status-colored top bar for dashboard and admin overview
- Added timeline component for status history shared across Admin, Manager, Engineer, and Support detail pages
- Implemented fully responsive layout: collapsing sidebar drawer on tablet/mobile, reflowing stat grids, single-column detail views on small screens
- Redesigned login, register, and admin-setup pages as centered cards on a dark background
- Redesigned home page as a two-column landing view with a custom infrastructure provisioning topology diagram
- Added centered footer with copyright notice to home page and sidebar on all logged-in pages