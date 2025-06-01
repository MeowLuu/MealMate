# s25_team_9
Repository for s25_team_9
MealMate - Project Specification
Product Owner for Sprint 1: Ria Wang (Andrew ID: yerouw)
1. Product Backlog
The following features define the complete functionality of MealMate. These are grouped into key modules.
1.1 User Authentication & Profiles
•	User Registration & Login (Django Auth/OAuth) 
o	Users can sign up/log in using email and password.
o	OAuth-based authentication (Google login) may be added if time permits.
•	User Profiles 
o	Users can update profile details (name, contact info, profile picture).
o	Users can view other participants’ profiles in events.
1.2 Meal Event Management
•	Create Dining Event 
o	Users can create meal events specifying: 
	Event Name
	Time & Date
	Location (Google Maps API)
	Max Participants
	Privacy (Public/Invite-Only)
•	Join Meal Event 
o	Users can browse & join available events.
o	Event creators can manage attendance (remove users, close event).
•	Location-based Event Recommendations 
o	Nearby meal events are suggested based on the user’s location.
o	Sorting based on proximity and popularity.
1.3 Bill Splitting & Payment
•	Equal or Custom Bill Splitting 
o	Organizers can enable an “AA Split” (Equal Cost Sharing) mode.
o	Users can specify custom amounts if needed.
•	Payment Integration (Stripe/PayPal API) 
o	Users can make payments within the app.
o	Payment status (Pending/Completed) is tracked.
1.4 Real-Time Group Chat
•	WebSocket-powered chatrooms 
o	Users are automatically added to a chatroom after joining an event.
o	Participants can discuss logistics, confirm attendance, and chat before the meal.









Task Allocation
Feature	Description	Tasks	Deliverables	Assigned To
User Registration & Login	Implement Django authentication system, allowing users to sign up and log in securely.	- Set up Django authentication model
- Create API endpoints for registration/login
- Implement session-based authentication	- Working registration/login API
- User authentication flow tested	Lu
Profile Management	Allow users to update their profile details, including name, picture, and dietary preferences.	- Create Django model for user profile
- Implement profile update API
- Add UI for profile editing	- Profile update page
- Backend API for updating profile	Lu
Create Meal Event	Users can create meal events by specifying details such as location, time, and participants.	- Design event creation model
- Build API for event creation
- Validate event form fields	- API for creating events
- Basic event creation UI	Ria
Join Event	Users can browse available events and join them.	- Implement API for joining events
- Update event participant count
- UI for browsing & joining events	- API for joining events
- Event list page	Ria
Basic UI Layout	Implement homepage and event details page UI.	- Design basic UI with placeholders
- Set up navigation and routing
- Display event details	- Homepage & event details page	Lu
Database Setup	Define Django models for users & events.	- Create models for User, Event, Profile
- Migrate database and test schema	- models.py file
- Working database schema	Lu
User Location Handling	Store user’s current location (manually set or auto-detected).	- Add location fields in User model
- Implement API for updating user location
- Allow users to set location manually	- API for storing user location
- Profile location settings	Lu
Google Maps API Integration	Display meal event locations on an interactive map.	- Set up Google Maps API / OpenStreetMap
- Show meal events on the map
- Add clickable markers for event details	- Interactive event map
- Location-based search	Lu
Nearby Event Recommendations	Recommend meal events based on user location.	- Implement geolocation-based filtering
- Fetch and display nearest events
- Optimize query performance	- 'Nearby Events' section in homepage
- Location-based search API	Ria
Bill Splitting & Payments	Allow event organizers to enable bill splitting and let users pay online or manually.	- Implement payment model
- Integrate Stripe/PayPal API
- Allow users to manually mark payments	- Bill splitting UI & backend
- Payment transaction records	Ria
Payment Status Updates	Update users' payment status in real-time when they complete transactions.	- Use WebSocket to update payment status
- Notify users when a payment is completed
- Display outstanding balances	- Live payment updates via WebSocket
- Payment confirmation notifications	Ria

 
2. First Sprint Backlog
For the first sprint, we focus on core functionalities while keeping the workload reasonable. Live chat and payments will not be implemented in this sprint. Instead, we focus on user authentication, event creation/joining, and data modeling validation.
Sprint 1 Deliverables
2.1 Backend Setup & Database Design
•	Django Backend Setup 
o	Initialize the project with Django.
o	Set up basic project structure.
•	Database Schema & ER Diagram Finalization 
o	ER diagram validation before implementing models (to prevent rework).
o	Once confirmed, implement core models in Django.
2.2 Frontend Setup

2.3 User Authentication & Profiles
•	User Registration & Login 
o	Implement Django authentication.
o	Create sign-up and login views.
•	User Profile Management 
o	Implement basic profile editing.
2.4 Meal Event Management
•	Create Meal Event (Basic) 
o	Implement event creation with form validation.
o	Store event details in the database.
•	Join Meal Event 
o	Implement event joining functionality.
Deferred to Future Sprints
•	Meal Event Management
•	Bill splitting & payments
•	OAuth integration (Google login)
•	Event recommendations (location-based)
•	Live chat (WebSocket)
Task Allocation
•	Ria Wang: Meal Creation, Event Joining, Bill Splitting & Payments Authentication 
•	Xiangning Lu: Database Setup/ER Diagram Refinement, User Registration & Login, Basic UI Layout, User Profiles




 

3. Data Models (Work-in-Progress)
As models are still being refined, this section is subject to updates after ER diagram validation. Below is a rough version:
User Model
class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True)
Event Model
class Event(models.Model):
    title = models.CharField(max_length=100)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    max_participants = models.IntegerField()
    participants = models.ManyToManyField(User, related_name="joined_events")
    status = models.BooleanField(default=True)  # Active or Canceled
Payment Model (Future Sprint)
Not implemented in Sprint 1.
