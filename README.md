Customer Relationship Manager API Description

This API provides a comprehensive set of endpoints for managing core aspects of a Customer Relationship Management (CRM) system. It allows you to interact with and manipulate data related to contacts, companies, activities, user accounts, and generate insightful reports.   

Core Functionality:

Contact Management: Create, retrieve, update, and manage information about individual contacts, including their personal details, company affiliation, category (lead, prospect, customer), and notes. Assign contacts to specific users for follow-up.

Company Management: Create, retrieve, update, and manage information about organizations, including their name, address, website, and other relevant details.

Activity Management: Track various interactions and tasks related to contacts, such as calls, emails, meetings, tasks, and general notes. Schedule due dates for tasks and activities, mark them as complete, and assign them to users.   

User Management: Handle user accounts, including registration, login (generating authentication tokens), profile management (retrieving and updating user details), password changes, and logout (invalidating authentication tokens).

Reporting: Generate valuable insights through various reports, including a sales funnel breakdown (contacts by category), the number of contacts created per month, and a list of recent activities.

Task Reminders: The system automatically sends email notifications for upcoming and overdue tasks to the assigned users, ensuring timely follow-up.





Key Features:

RESTful Design: The API adheres to RESTful principles, utilizing standard HTTP methods (GET, POST, PUT, PATCH, DELETE) for performing actions on resources. 

JSON Data Format: All requests and responses utilize the JSON (JavaScript Object Notation) data format for easy parsing and interoperability.

Token-Based Authentication: Secure access to protected endpoints is managed through token-based authentication. Users obtain a unique token upon successful login, which must be included in the Authorization header of subsequent requests.

Granular Permissions: Access control is implemented through refined permission classes, ensuring that users can only interact with data they are authorized to manage. This includes allowing assigned users and managers to modify contacts and activities, and managers having extended privileges like reassigning users and extending due dates.

Filtering, Pagination, Ordering, and Searching: List endpoints support various query parameters to filter, paginate, order, and search through collections of resources, allowing for efficient data retrieval.

Soft Deletes: For contacts and activities, a soft delete mechanism is implemented. Instead of permanent deletion, records are marked as is_deleted, preserving data integrity and potential for recovery. Companies are currently hard-deleted.

API Root: A dedicated /api/ endpoint provides a discoverable entry point, listing the available API endpoints.






Here is  a breakdown of each API endpoint, along with example data and descriptions you can use to test them. Replace placeholders and example data with actual values.

Authentication:

POST /users/login/
Description: Logs in a user and returns an authentication token.
Body (raw - JSON):
JSON

{
   "username": "",
   "password": ""
}
Expected Response: 200 OK with a JSON body containing the key (the authentication token).


POST /users/logout/
Description: Logs out the currently authenticated user by invalidating their token.
Headers: Include Authorization: Token YOUR_AUTH_TOKEN.
Expected Response: 200 OK with a JSON body: 
JSON
{
    "message": "Successfully logged out."
}


User Management:

POST /users/register/
Description: Registers a new user.
Body (raw - JSON):
JSON
{
    "username": " ",
    "email": " ",
    "first_name": " ",
     "last_name": " ",
     "password": " ",
      "password2": " "
}
Expected Response: 201 Created with user details.

GET /users/profile/
Description: Retrieves the profile of the currently authenticated user.
Headers: Include Authorization: Token YOUR_AUTH_TOKEN.
Expected Response: 200 OK with user profile information (job_title, location, profile_pic).

PUT /users/profile/ or PATCH /users/profile/
Description: Updates the profile of the currently authenticated user.
Headers: Include Authorization: Token YOUR_AUTH_TOKEN 
Content-Type: application/json.
Body (raw - JSON):
JSON

{
    "job_title": " ",
    "location": " "
}
Expected Response: 200 OK with the updated user profile information.

PUT /users/password/change/
Description: Changes the password of the currently authenticated user.
Headers: Include Authorization: Token YOUR_AUTH_TOKEN  
Content-Type: application/json.
Body (raw - JSON):
JSON

{
    "old_password": " ",
    "new_password1": " ",
    "new_password2": " "
}
Expected Response: 200 OK with a JSON body:
JSON

{
    "message": "Password updated successfully."
}


Contacts:

GET /contacts/
Description: Lists all non-deleted contacts (with optional query parameters for filtering, pagination, etc.).
Headers: Include Authorization: Token YOUR_AUTH_TOKEN.
Optional Query Parameters:
category: lead, prospect, customer
company: (Company ID)
assigned_to: (User ID)
page: (page number)
page_size: (number of contacts per page)
ordering: first_name, -created_at, etc.
search: (search term)
Expected Response: 200 OK with a paginated list of contact objects.

POST /contacts/
Description: Creates a new contact.
Headers: Include Authorization: Token YOUR_AUTH_TOKEN 
Content-Type: application/json.
Body (raw - JSON):
JSON

{
    "first_name": " ",
    "last_name": " ",
    "email": " ",
    "phone_number": " ",
    "company":  ,
    "category": " ",
    "notes": " "
}
Expected Response: 201 Created with the newly created contact object.


GET /contacts/{id}/
Description: Retrieves a specific contact by ID.
Headers: Include Authorization: Token YOUR_AUTH_TOKEN.
Path Parameter: Replace {id} with the ID of the contact.
Expected Response: 200 OK with the contact object.


PUT /contacts/{id}/ or PATCH /contacts/{id}/
Description: Updates a specific contact by ID.
Headers: Include Authorization: Token YOUR_AUTH_TOKEN and 
Content-Type: application/json
Path Parameter: Replace {id} with the ID of the contact.
Body (raw - JSON):
JSON

{
    "email": " ",
    "category": " "
}
Expected Response: 200 OK with the updated contact object.

DELETE /contacts/{id}/
Description: Soft deletes a specific contact by ID.
Headers: Include Authorization: Token YOUR_AUTH_TOKEN.
Path Parameter: Replace {id} with the ID of the contact.
Expected Response: 204 No Content.


Companies:

GET /companies/
Description: Lists all companies (with optional query parameters).
Headers: Include Authorization: Token YOUR_AUTH_TOKEN.
Optional Query Parameters: name, city, country, page, page_size, ordering, search.
Expected Response: 200 OK with a paginated list of company objects.


POST /companies/
Description: Creates a new company (requires staff user).
Headers: Include Authorization: Token YOUR_AUTH_TOKEN (for a staff user) and Content-Type: application/json.
Body (raw - JSON):
JSON

{
    "name": " ",
    "address": " ",
    "city": " ",
    "country": " “
    "website": " "
}
Expected Response: 201 Created with the newly created company object.


GET /companies/{id}/
Description: Retrieves a specific company by ID.
Headers: Include Authorization: Token YOUR_AUTH_TOKEN.
Path Parameter: Replace {id} with the ID of the company.
Expected Response: 200 OK with the company object.





PUT /companies/{id}/ or PATCH /companies/{id}/
Description: Updates a specific company by ID (requires staff user).
Headers: Include Authorization: Token YOUR_AUTH_TOKEN (for a staff user) and Content-Type: application/json.
Path Parameter: Replace {id} with the ID of the company.
Body (raw - JSON):
JSON

{
    "website": ""
}
Expected Response: 200 OK with the updated company object.


DELETE /companies/{id}/
Description: Hard deletes a specific company by ID (requires staff user).
Headers: Include Authorization: Token YOUR_AUTH_TOKEN (for a staff user).
Path Parameter: Replace {id} with the ID of the company.
Expected Response: 204 No Content.


Activities

GET /activities/
Description: Lists all non-deleted activities (with optional query parameters).
Headers: Include Authorization: Token YOUR_AUTH_TOKEN.
Optional Query Parameters: activity_type, subject, completed, priority, assigned_to, contact, due_date, page, limit, offset, ordering, search.
Expected Response: 200 OK with a paginated list of activity objects.


POST /activities/
Description: Creates a new activity.
Headers: Include Authorization: Token YOUR_AUTH_TOKEN 
Content-Type: application/json.
Body (raw - JSON):
JSON

{
    "contact": ,
    "activity_type": " ",
    "subject": " ",
    "details": " .",
    "due_date": " "
}
Expected Response: 201 Created with the newly created activity object.


GET /activities/{id}/
Description: Retrieves a specific activity by ID.
Headers: Include Authorization: Token YOUR_AUTH_TOKEN.
Path Parameter: Replace {id} with the ID of the activity.
Expected Response: 200 OK with the activity object.


PUT /activities/{id}/ or PATCH /activities/{id}/
Description: Updates a specific activity by ID.
Headers: Include Authorization: Token YOUR_AUTH_TOKEN 
Content-Type: application/json.
Path Parameter: Replace {id} with the ID of the activity.
Body (raw - JSON):
JSON

{
    "completed": ,
    "due_date": " "
}
Expected Response: 200 OK with the updated activity object.



DELETE /activities/{id}/
Description: Soft deletes a specific activity by ID.
Headers: Include Authorization: Token YOUR_AUTH_TOKEN.
Path Parameter: Replace {id} with the ID of the activity.
Expected Response: 204 No Content.


GET /contacts/{contact_id}/activities/
Description: Lists activities associated with a specific contact.
Headers: Include Authorization: Token YOUR_AUTH_TOKEN.
Path Parameter: Replace {contact_id} with the ID of the contact.
Optional Query Parameters: activity_type, subject, completed, ordering.
Expected Response: 200 OK with a list of activity objects.




POST /contacts/{contact_id}/activities/
Description: Creates a new activity associated with a specific contact.
Headers: Include Authorization: Token YOUR_AUTH_TOKEN and Content-Type: application/json.
Path Parameter: Replace {contact_id} with the ID of the contact.
Body (raw - JSON): (Same as POST /activities/ but contact field in body is not needed as it's inferred from the URL).
Expected Response: 201 Created with the newly created activity object.
Tasks:

GET /tasks/
Description: Lists all non-deleted activities with activity_type as 'task'.
Headers: Include Authorization: Token YOUR_AUTH_TOKEN.
Optional Query Parameters: Same as GET /activities/.
Expected Response: 200 OK with a paginated list of task objects.
Reports:



Reports
GET /reports/sales/
Description: Retrieves the sales funnel report (counts of contacts by category).
Headers: Include Authorization: Token YOUR_AUTH_TOKEN.
Expected Response: 200 OK with a JSON object like:
JSON

{
    "lead": 10,
    "prospect": 5,
    "customer": 20
}


GET /reports/contacts_created_by_month/
Description: Retrieves the report of contacts created per month (optional year query parameter).
Headers: Include Authorization: Token YOUR_AUTH_TOKEN.
Optional Query Parameter: year (e.g., year=2025).
Expected Response: 200 OK with a JSON object like:
JSON

{
    "2025-03": 5,
    "2025-04": 12
}


GET /reports/recent_activities/
Description: Retrieves the most recent activities (optional limit query parameter).
Headers: Include Authorization: Token YOUR_AUTH_TOKEN.
Optional Query Parameter: limit (e.g., ?limit=5).
Expected Response: 200 OK with a list of recent activity objects.


API Root:

GET /
Description: Lists the available API endpoints.
Expected Response: 200 OK with a JSON object containing the URLs of the main endpoints.

Remember to start your Django development server (python manage.py runserver) when testing locally. 
