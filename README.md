# User Documentation

## Project Description
```sh
DriftDater is a dating website that allows for users to connect with each other based on mutual interests and proximity.

When first starting, a user gives their information, the most important of which for finding love being their location, relationship and interests.
From there, the system suggests the potential matches through filtering the users based on how close they are to the user and if they have shared interests.
If there are mutual positive interactions, then the users get matched together.

```

## Team Members

#### Hayden Byfield (620157453)
##### Roles:
```sh
Project Manager
Database Design and Management
Backend development for Matching, Interactions, Favourites, Location
Testing
```
#### Justine Lewis (620165751)
##### Roles:
```sh
Frontend development for User Authentication and Profile Management, Home, Dashboard
Testing
```
#### Keanu Thompson (620144490)
##### Roles:
```sh
Frontend development for Dashboard, Matching and Messages
User Manual
Testing
```
#### Dejone Watson (620155149)
##### Roles:
```sh
Backend development for User Authentication and Profile Management
User Documentation
ER Diagramming 
Testing
```
## Setup Instructions

#### Clone the Repository
```sh
$ git clone <repository-url>
$ cd Info3180_GroupProject
```
#### Create and Activate Virtual Environment
```sh
$ python -m venv venv
$ .\venv\Scripts\activate
```
#### Install Backend Dependencies
```sh
$ pip install -r requirements.txt
```
#### Configure Environment Variables
```sh
$ FLASK_APP=app.py
$ FLASK_ENV=development
$ SECRET_KEY=your_secret_key
$ DATABASE_URL=mysql://username:password@localhost/driftdater
$ UPLOAD_FOLDER=uploads
```
#### Create Database
```sh
$ CREATE DATABASE driftdater;

$ SQL Shell inputs below:

$ create user "admin_user"; 
$ create database "driftdater"; 
$ \password admin_user 
$ alter database driftdate owner to admin_user; 
```
#### Run Database Migrations
```sh
$ Once you create routing of your database in the app and create your first table and connect to the database on pgAdmin4 then run:

$ flask db init
$ flask db migrate
$ flask db upgrade 
```
#### Start Flask Backend
```sh
$ flask --app app --debug run
```
#### Install Frontend Dependencies
```sh
$ npm install
```
#### Start Vue Development Server
```sh
$ npm run dev
```
#### Configure Vite Proxy
```sh
$ server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8080',
      changeOrigin: true
    }
  }
}
```
## Known Issues and Limitations

## API Documentation

Most write requests require a CSRF token. Fetch `GET /api/csrf-token` first and send the returned token in the `X-CSRFToken` header for `POST`, `PUT`, and `PATCH` requests. Endpoints marked "Requires login" use the current Flask-Login session.

#### Get CSRF Token
```http
GET /api/csrf-token
```
Description: Returns a CSRF token for protected requests.

Response:
```json
{
  "csrf_token": "token-value"
}
```

#### Get Current User
```http
GET /api/me
```
Requires login.

Description: Returns the logged-in user's account and profile information.

Response:
```json
{
  "id": 1,
  "username": "Jordan",
  "email": "jordan@example.com",
  "profile": {
    "name": "Jordan Smith",
    "age": 22,
    "location": "Kingston",
    "bio": "I love music and coffee.",
    "relationship": "Long-term",
    "occupation": "Student",
    "photo": "jordan.jpg"
  }
}
```

#### Register User
```http
POST /api/users
```
Description: Creates a new user account, saves the user's latitude and longitude, and logs the user in.

Request JSON:
```json
{
  "username": "Jordan",
  "email": "jordan@example.com",
  "password": "password123",
  "confirmpassword": "password123",
  "latitude": 18.0179,
  "longitude": -76.8099
}
```

Success response:
```json
{
  "success": true,
  "message": "User created"
}
```

Error responses include:
```json
{ "success": false, "message": "No JSON received" }
{ "success": false, "message": "Passwords must match" }
{ "success": false, "message": "Email already in use" }
{ "success": false, "message": "User already exists" }
```

#### Login User
```http
POST /api/login
```
Description: Authenticates a user by email and password.

Request JSON:
```json
{
  "email": "jordan@example.com",
  "password": "password123"
}
```

Success response:
```json
{
  "success": true
}
```

Error responses include:
```json
{ "success": false, "message": "Account does not exist" }
{ "success": false, "message": "Incorrect password" }
```

#### Logout User
```http
POST /api/logout
```
Requires login.

Description: Logs out the current user.

Response:
```json
{
  "success": true,
  "message": "User Logged Out"
}
```

#### Create Profile
```http
POST /api/profile
```
Requires login.

Description: Creates the logged-in user's profile, preferences, profile photo, and interests.

Request form data:
```text
name=Jordan Smith
age=22
location=Kingston
relationshipGoal=Long-term
bio=I love music and coffee.
occupation=Student
radius=20
interests=["Music","Coffee"]
profilePhoto=<image file>
```

Response:
```json
{
  "success": true,
  "message": "Profile Created"
}
```

#### Update Profile
```http
PUT /api/profile
```
Requires login.

Description: Updates the logged-in user's profile, preferences, interests, and optional profile photo.

Request form data:
```text
name=Jordan Smith
age=23
location=Kingston
relationshipGoal=Long-term
bio=Updated bio text.
occupation=Developer
radius=30
interests=["Music","Travel"]
profilePhoto=<optional image file>
```

Success response:
```json
{
  "success": true,
  "message": "Profile Updated"
}
```

Error response:
```json
{
  "success": false,
  "message": "Profile does not exist"
}
```

#### Update User Location
```http
PATCH /api/location
```
Requires login.

Description: Updates the logged-in user's GPS coordinates.

Request JSON:
```json
{
  "latitude": 18.0179,
  "longitude": -76.8099
}
```

Response:
```json
{
  "message": "Location Updated"
}
```

#### Get Potential Matches
```http
GET /api/matches
```
Requires login.

Description: Returns users whose distance is within both the current user's radius and the other user's radius.

Response:
```json
[
  {
    "id": 4,
    "username": "Ashley",
    "email": "ashley@example.com",
    "latitude": 18.0123,
    "longitude": -76.8001,
    "radius": 15,
    "photo": "ashley.jpg",
    "bio": "Beach days and books.",
    "age": 24,
    "location": "Kingston",
    "distance": 5.2
  }
]
```

#### Add Interaction
```http
POST /api/interact
```
Requires login.

Description: Saves a `like` or `pass` interaction. If two users like each other, a chat room is created automatically.

Request JSON:
```json
{
  "user_id": 4,
  "action": "like"
}
```

Response:
```json
{
  "message": "Interaction Complete"
}
```

#### Get Mutual Matches
```http
GET /api/interact
```
Requires login.

Description: Returns users who have mutual likes with the logged-in user.

Response:
```json
[
  {
    "id": 4,
    "user_id": 4,
    "username": "Ashley",
    "age": 24,
    "location": "Kingston",
    "bio": "Beach days and books.",
    "photo": "ashley.jpg",
    "interests": ["Music", "Travel"],
    "chatroom_id": 1
  }
]
```

#### Add Favourite
```http
POST /api/favourite
```
Requires login.

Description: Adds another user to the logged-in user's favourites list.

Request JSON:
```json
{
  "user_id": 4
}
```

Success response:
```json
{
  "message": "Successfully Added Favourites"
}
```

Duplicate response:
```json
{
  "message": "Favourite already added"
}
```

#### Get Favourites
```http
GET /api/favourite
```
Requires login.

Description: Returns all users favourited by the logged-in user.

Response:
```json
{
  "favourite": [
    {
      "id": 4,
      "username": "Ashley",
      "age": 24
    }
  ]
}
```

#### Get Chatrooms
```http
GET /api/chats
```
Requires login.

Description: Returns all chat rooms associated with the logged-in user.

Response:
```json
[
  {
    "chatroom_id": 1,
    "user_id": 4,
    "username": "Ashley"
  }
]
```

#### Send Message
```http
POST /api/message
```
Requires login.

Description: Stores a message in a chat room.

Request JSON:
```json
{
  "chatroom_id": 1,
  "message": "Hey!"
}
```

Response:
```json
{
  "Message": "Successfully stored message in the database"
}
```

#### Get Messages
```http
GET /api/message/<chatroom_id>
```
Requires login.

Description: Returns all messages for a chat room ordered by message ID.

Response:
```json
[
  {
    "sender_id": 2,
    "message": "Hey!",
    "chatroom_id": 1
  }
]
```

#### Search Users
```http
GET /api/search?age_min=18&age_max=30&interest=Music&radius=1&matches=false&sort=newest
```
Requires login.

Description: Searches profiles using optional age, interest, distance, mutual-match, and sort filters.

Query parameters:
```text
age_min: minimum profile age
age_max: maximum profile age
interest: exact interest name
radius: when present, limits results to the current user's saved radius
matches: true to return only mutual matches
sort: newest or oldest
```

Response:
```json
{
  "result": [
    {
      "id": 4,
      "username": "Ashley",
      "age": 24,
      "bio": "Beach days and books.",
      "location": "Kingston",
      "photo": "ashley.jpg",
      "distance": 5.2
    }
  ]
}
```

#### Get Uploaded Profile Photo
```http
GET /uploads/<filename>
```
Description: Serves an uploaded profile photo by filename.

# INFO3180 VueJS and Flask Starter

This template should help get you started developing with Vue 3 on the frontend and Flask as an API on the backend.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.vscode-typescript-vue-plugin).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

## Start Flask API

Remember to always create a virtual environment and install the packages in your requirements file

```bash
$ python -m venv venv (you may need to use python3 instead)
$ source venv/bin/activate (or .\venv\Scripts\activate on Windows)
$ pip install -r requirements.txt
$ flask --app app --debug run
# Create Secret Key
$ python -c 'import secrets; print(secrets.token_hex())'

$ pip install python-dotenv
$ pip install flask-sqlalchemy
$ pip install flask-migrate
$ pip install flask-wtf
```
