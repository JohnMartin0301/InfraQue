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