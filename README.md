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

#### Create Profile
```sh
$ POST /api/profile
$ response:
{
  "success": true,
  "message": "Profile Updated"
}
$ Description: 
$ Creates a user profile, uploads a profile photo, stores preferences, and assigns interests.
```
#### Edit Profile
```sh
$ POST /api/editprofile
$ response:
{
  "success": true,
  "message": "Profile Edited"
}
$ Description: 
$ Updates an existing user profile, preferences, interests, and optional profile image.
```
#### Update User Location
```sh
$ POST /api/updatelocation
$ response:
{
  "message": "Location Updated"
}
$ Description: 
$ Updates the logged-in user's GPS coordinates.
```
#### Get Potential Matches
```sh
$ GET /api/matches
$ response:
[
  {
    "id": 4,
    "username": "Ashley",
    "distance": 5.2
  }
]
$ Description: 
$ Returns nearby users based on geographic distance and user radius preferences.
```
#### Login User
```sh
$ POST /api/login
$ response:
{
  "success": true
}
{
  "success": false,
  "message": "Account does not exist"
}
{
  "success": false,
  "message": "Incorrect password"
}
$ Description: 
$ Authenticates a user using email and password.
```
#### Register User
```sh
$ POST /api/registration
$ response:
{
  "success": true,
  "message": "User created"
}
{
  "success": false,
  "message": "Passwords must match"
}
{
  "success": false,
  "message": "Email already in use"
}
{
  "success": false,
  "message": "User already exists"
}
$ Description: 
$ Creates a new user account and logs the user in.
```

#### Logout User
```sh
$ GET /api/logout
$ response:
{
  "success": true,
  "message": "User Logged Out"
}
$ Description: 
$ Logs out the currently authenticated user.
```

#### Get Mutual Matches
```sh
$ GET /api/interact
$ response:
[
  {
    "user_id": 7
  }
]
$ Description: 
$ Returns users who mutually liked each other and automatically creates a chatroom.
```
#### Add Favorite
```sh
$ POST /api/favorite
$ response:
{
  "messsage": "Successfully Added Favourties"
}
$ Description: 
$ Adds another user to the current user's favorites list.
```
#### Get Favorites
```sh
$ GET /api/favorites
$ response:
{
  "favourite": [
    {
      "id": 2,
      "username": "Jordan",
      "age": 22
    }
  ]
}
$ Description: 
$ Returns all users favorited by the current user.
```
#### Get Chatrooms
```sh
$ GET /api/getChat
$ response:
[
  {
    "chatroom_id": 1,
    "user_id": 5,
    "username": "Ashley"
  }
]
$ Description: 
$ Returns all chatrooms associated with the current user.
```
#### Send Message
```sh
$ POST /api/message
$ response:
{
  "Message": "Successfully stored message in the database"
}
$ Description: 
$ Stores a message inside a chatroom.
```

#### Get Messages
```sh
$ GET /api/message/<chatroom_id>
$ response:
[
  {
    "sender_id": 2,
    "message": "Hey!",
    "chatroom_id": 1
  }
]
$ Description: 
$ Returns all messages for a specific chatroom ordered by timestamp.
```

#### Search Users
```sh
$ GET /api/search
$ response:
{
  "result": [
    {
      "id": 4,
      "username": "Chris",
      "age": 21
    }
  ]
}
$ Description: 
$ Searches for users using filters such as age range, interests, distance, and matches. ordered by timestamp.
```

## Known Issues and Limitations
```sh
Difficulties in regards to integration may lead to failure of frontend data reaching backend. Independently, these are functional methods but currently unable to locate source of failure 
```

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
