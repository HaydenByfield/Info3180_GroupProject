"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""
import os
import json
from app import app, db, login_manager, csrf
from flask import render_template, request, jsonify, send_file
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import text, func
from werkzeug.utils import secure_filename
from app.models import Interactions, Users, Preferences, UserInterests, Interest, Favorite, Chat, ChatRoom, Profile
from flask_wtf.csrf import generate_csrf

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


#works
@app.route('/api/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})


#works
@app.route('/api/me', methods=['GET'])
@login_required
def get_current_user():
    profile = Profile.query.filter_by(user_id=current_user.id).first()

    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'profile': {
            'name': profile.name if profile else None,
            'age': profile.age if profile else None,
            'location': profile.location if profile else None,
            'bio': profile.Bio if profile else None,
            'relationship': profile.relationship if profile else None,
            'occupation': profile.occupation if profile else None,
            'photo': profile.photo if profile else None
        } if profile else None
    })


#works
@app.route('/api/users', methods=['POST'])
def register_user():
    data = request.get_json() 
    if not data:
        return jsonify({"success": False, "message": "No JSON received"}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirmpassword = data.get('confirmpassword')

    user = Users.query.filter_by(username=username).first()
    emailcheck = Users.query.filter_by(email=email).first()

    if user is None:
        if password != confirmpassword:
            return jsonify({'success': False, 'message': 'Passwords must match'})
        if emailcheck:
            return jsonify({'success': False, 'message': 'Email already in use'})
        
        newuser = Users(
            username = username,
            email = email,
            password = password,
        )

        newuser.latitude = data.get('latitude')
        newuser.longitude = data.get('longitude')

        db.session.add(newuser)
        db.session.commit()

        login_user(newuser)
        return jsonify({'success': True, 'message': 'User created'})
        
    else:
        return jsonify({'success': False, 'message': 'User already exists'})


#works
@app.route('/api/login', methods = ['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = Users.query.filter_by(email=email).first()

    if user is None:
        return jsonify({'success': False, 'message': 'Account does not exist'}), 404

    if user and user.check_password(password):
        login_user(user)
        return jsonify({'success': True}), 200

    return jsonify({'success': False, 'message': 'Incorrect password'}), 401


#works
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'success': True, 'message': 'User Logged Out'})


#works
@app.route('/api/profile', methods=['POST'])
@login_required
def create_profile():
    name = request.form.get('name')
    age = request.form.get('age')
    location = request.form.get('location')
    relationship = request.form.get('relationshipGoal')
    bio = request.form.get('bio')
    occupation = request.form.get('occupation')
    interests = request.form.get('interests')
    radius = request.form.get('radius')
    photo = request.files.get('profilePhoto')

    if photo:
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    interests_list = json.loads(interests)
    
    user_profile = Profile(
        user_id = current_user.id,
        name = name,
        age = age,
        location = location,
        relationship = relationship,
        Bio = bio,
        occupation = occupation,
        photo = filename
    )
    db.session.add(user_profile)

    user_preferences = Preferences(
        user_id=current_user.id,
        radius=radius
    )

    db.session.add(user_preferences)

    for interest_name in interests_list:
        existing_interest = Interest.query.filter_by(name=interest_name).first()
        if not existing_interest:
            existing_interest = Interest(
                name = interest_name
            )
            db.session.add(existing_interest)
            db.session.flush()

        user_interest = UserInterests(
            user_id = current_user.id,
            interest_id = existing_interest.id
        )
        db.session.add(user_interest) #adds user to database
    db.session.commit() #saves user

    return jsonify({'success': True, 'message': 'Profile Created'})


#works
@app.route('/api/profile', methods=['PUT'])
@login_required
def update_profile():
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if profile is None:
        return jsonify({'success': False, 'message': 'Profile does not exist'}), 404

    name = request.form.get('name')
    age = request.form.get('age')
    location = request.form.get('location')
    relationship = request.form.get('relationshipGoal')
    bio = request.form.get('bio')
    occupation = request.form.get('occupation')
    interests = request.form.get('interests')
    radius = request.form.get('radius')
    photo = request.files.get('profilePhoto')

    if photo:
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        profile.photo = filename

    profile.name = name
    profile.age = age
    profile.location = location
    profile.relationship = relationship
    profile.Bio = bio
    profile.occupation = occupation

    user_preferences = Preferences.query.filter_by(user_id=current_user.id).first()
    if user_preferences:
        user_preferences.radius = radius
    else:
        user_preferences = Preferences(
            user_id=current_user.id,
            radius=radius
        )
        db.session.add(user_preferences)

    UserInterests.query.filter_by(user_id=current_user.id).delete()
    interests_list = json.loads(interests)

    for interest_name in interests_list:
        existing_interest = Interest.query.filter_by(name=interest_name).first()
        if not existing_interest:
            existing_interest = Interest(name=interest_name)
            db.session.add(existing_interest)
            db.session.flush()

        user_interest = UserInterests(
            user_id=current_user.id,
            interest_id=existing_interest.id
        )
        db.session.add(user_interest)

    db.session.commit()

    return jsonify({'success': True, 'message': 'Profile Updated'})


@app.route('/api/location', methods=['PATCH'])
@login_required
def updateLocation():
    data = request.get_json()

    current_user.latitude = data['latitude']
    current_user.longitude = data['longitude']
    db.session.commit()

    return jsonify({'message' : "Location Updated"})


#works
@app.route('/api/matches', methods=['GET'])
@login_required
def get_matches():
    """
    Calculates the Total distance in km, using the current_user's and other user's longitude and latitude
    Then Joins the preferences table to get the users radius from preferences
    Allows the distance calculation from a specific table be a sub query 
    Gets the users who radius falls within your range and you within their range
    """
    query = text("""SELECT * FROM
                            (SELECT u.id, u.username, u.email, u.latitude, u.longitude, p.radius,
                            (6371 * acos
                                (cos(radians(:lat1)) * cos(radians(u.latitude)) *
                                cos(radians(u.longitude) - radians(:lon1)) +
                                sin(radians(:lat1)) * sin(radians(u.latitude))
                    )) AS distance
                    FROM user_profile u
                    JOIN preferences_profile p ON u.id = p.user_id
                    WHERE u.id != :current_user_id
                ) AS sub
                WHERE distance <= :my_radius
                AND distance <= sub.radius
                """)
    # Runs and Executes SQL query and supplies values for SQL placeholders e.g(lat1) and returns all rows
    results = db.session.execute(query,{
        'lat1' : current_user.latitude,
        'lon1' : current_user.longitude,
        'current_user_id': current_user.id,
        'my_radius' : current_user.preference.radius
        }).fetchall()
    return jsonify([dict(user._mapping) for user in results])


#works
@app.route('/api/interact', methods=['POST'])
@login_required
def add_interaction():
    # Retrieve data from json body
    data = request.get_json()
    
    # Creates a group of the current_user's interactions based on who he interacted with
    interaction = Interactions(
        from_user = current_user.id,
        to_user = data['user_id'], 
        action = data['action']
    )
    # Add the favourited user to the database
    db.session.add(interaction)
    db.session.commit()

    # check for mutual like and create chatroom if there is a match
    if data['action'] == 'like' and checkMutualLikes(current_user.id, data['user_id']):
        createChat(current_user.id, data['user_id'])

    return jsonify({'message': "Interaction Complete"})

def checkMutualLikes(user1, user2):
    # Check if the user1 liked user2
    interact_1 = Interactions.query.filter_by(
        from_user = user1, to_user = user2, action='like'
    ).first()
    # Checks if the user2 also liked user1
    interact_2 = Interactions.query.filter_by(
        from_user = user2, to_user = user1, action='like'
    ).first()
    # If both are true it returns a match otherwise returns false
    if interact_1 and interact_2:
        return True
    return False

def createChat(user1, user2):
    # Ensures no duplicate chatroom
    duplicate = ChatRoom.query.filter(
        ((ChatRoom.chat1_id == user1) & (ChatRoom.chat2_id == user2)) |
        ((ChatRoom.chat1_id == user2) & (ChatRoom.chat2_id == user1))
    ).first()

    # Creates a Chatroom and Stores it in the database
    if not duplicate:
        room = ChatRoom (
            chat1_id = user1, 
            chat2_id = user2
        )
        db.session.add(room)
        db.session.commit()

    return jsonify({'Message':'ChatRoom was created'})


#OMIT THIS ROUTE
#OPT FOR: CHECK FOR MUTUAL LIKES IN THE INTERACT ROUTE AND THEN CREATE A CHATROOM IF THERE IS A MATCH
'''
@app.route('/api/interact', methods=['GET'])
@login_required
def matchMade():
    # Filters the Interactions list to find the the current users interactions as a list
    interact= Interactions.query.filter_by(from_user=current_user.id, action='like').all()
    matches = []
    # Loops through the lst for any data needed from the current users interactions
    for i in interact:
        # Checks if the current user Id and the id of the other user is a match
        if checkMutualConnections(current_user.id, i.to_user):
            createChat(current_user.id, i.to_user)
            # Create a list of matched users for the current_user
            matches.append({
                'user_id': i.to_user
            })
    return jsonify(matches), 200
'''


#works
@app.route('/api/favourite', methods=['POST'])
@login_required
def add_favourite():
    # Retrieve data from json body
    data = request.get_json()
    favorite_user_id = data['user_id']

    existing_favourite = Favorite.query.filter_by(
        user_id=current_user.id,
        favorite_id=favorite_user_id
    ).first()

    if existing_favourite:
        return jsonify({'message': 'Favourite already added'}), 409

    # Creates a group of the User who favourited and user who is being favourited
    fav = Favorite(
        user_id=current_user.id,
        favorite_id=favorite_user_id
    )
    # Add the favourited user to the database
    db.session.add(fav)
    db.session.commit()

    return jsonify({'message': 'Successfully Added Favourites'})


@app.route('/api/favourite', methods=['GET'])
@login_required
def get_favourites():
    favorite = db.session.query(Users, Profile).join(
        Favorite, Users.id == Favorite.favorite_id
    ).outerjoin(
        Profile, Profile.user_id == Users.id
    ).filter(
        Favorite.user_id == current_user.id
    ).all()

    f_lst = [
        {
            'id': user.id,
            'username': user.username,
            'age': profile.age if profile else None
        } for user, profile in favorite
    ]
    return jsonify({'favourite': f_lst})


#works
@app.route('/api/chats', methods=['GET'])
@login_required
def get_chats():
    # Filters for any chatroom with the current user
    rooms = ChatRoom.query.filter(
        (ChatRoom.chat1_id == current_user.id) |
        (ChatRoom.chat2_id == current_user.id)
    ).all()
    results = []
    # Loops through the filter, verfies which chatroom user the current user is then return the other_user based on that result
    for room in rooms:
        if room.chat1_id == current_user.id:
            other_user = room.chat2_id
        elif room.chat2_id == current_user.id:
            other_user = room.chat1_id
        
        # Gets the other users information from the user table
        user = Users.query.get(other_user)

        # Returns each specific Chat room for the current user
        results.append({
            'chatroom_id': room.id,
            'user_id': user.id,
            'username': user.username
        })
    return jsonify(results),200


#works
@app.route('/api/message', methods=['POST'])
@login_required
def send_message():
    data = request.get_json()

    # Creates a group chat data
    message = Chat(
        sender_id = current_user.id,
        chatroom_id = data['chatroom_id'],
        message = data['message']
    )
    # Adds the collected data back to the database
    db.session.add(message)
    db.session.commit()

    return jsonify({'Message':'Successfully stored message in the database'})


#works
@app.route('/api/message/<int:chatroom_id>', methods=['GET'])
@login_required
def get_message(chatroom_id):
    # Creates messages for a chatroom based url room selected and order each message accordingly 
    messages = Chat.query.filter_by(
        chatroom_id = chatroom_id
    ).order_by(Chat.id.asc()).all()

    # Store both users of the chatroom and there messages in a list of results
    result = [
        {
            "sender_id": m.sender_id,
            "message": m.message,
            "chatroom_id": m.chatroom_id
        } for m in messages
    ]
    return jsonify(result)


@app.route('/api/search', methods=['GET'])
@login_required
def search():
    # Collect all the search filters from the URL query string.
    age_min = request.args.get('age_min', type=int)
    age_max = request.args.get('age_max', type=int)
    interest = request.args.get('interest')
    use_distance = request.args.get('radius', type=float)
    matches = request.args.get('matches', '').lower() == 'true'
    sort = request.args.get('sort')

    distance = 6371 * func.acos(
        func.cos(func.radians(current_user.latitude)) *
        func.cos(func.radians(Users.latitude)) *
        func.cos(func.radians(Users.longitude) - func.radians(current_user.longitude)) +
        func.sin(func.radians(current_user.latitude)) *
        func.sin(func.radians(Users.latitude))
    )

    search_query = db.session.query(
        Users,
        Profile,
        distance.label('distance')
    ).join(
        Profile, Profile.user_id == Users.id
    ).filter(
        Users.id != current_user.id
    )

    # Filter by age using the profile table, where age is stored.
    if age_min is not None:
        search_query = search_query.filter(Profile.age >= age_min)
    if age_max is not None:
        search_query = search_query.filter(Profile.age <= age_max)

    # Filter by users connected to the requested interest.
    if interest:
        search_query = search_query.join(
            UserInterests, UserInterests.user_id == Users.id
        ).join(
            Interest, Interest.id == UserInterests.interest_id
        ).filter(
            Interest.name == interest
        )

    # Filter to users with mutual likes.
    if matches:
        liked_by_me = db.session.query(Interactions.to_user).filter(
            Interactions.from_user == current_user.id,
            Interactions.action == 'like'
        )
        liked_me = db.session.query(Interactions.from_user).filter(
            Interactions.to_user == current_user.id,
            Interactions.action == 'like'
        )
        search_query = search_query.filter(
            Users.id.in_(liked_by_me),
            Users.id.in_(liked_me)
        )

    if use_distance:
        radius = current_user.preference.radius
        search_query = search_query.filter(distance <= radius)
    
    # Apply sorting on search results.
    if sort =='newest':
        search_query = search_query.order_by(Users.id.desc())
    elif sort == 'oldest':
        search_query = search_query.order_by(Users.id.asc())
    
    # Return user account data together with profile fields.
    s_result = search_query.all()
    result = [{
        "id": user.id,
        "username": user.username,
        "age": profile.age,
        "bio": profile.Bio,
        "location": profile.location,
        "photo": profile.photo,
        "distance": round(calculated_distance, 2) if calculated_distance is not None else None
    } for user, profile, calculated_distance in s_result]

    return jsonify({'result': result}),200


@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(Users).filter_by(id=id)).scalar()


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
