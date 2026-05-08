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

## Known Issues and Limitations

## API Documentation

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
