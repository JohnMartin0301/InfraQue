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