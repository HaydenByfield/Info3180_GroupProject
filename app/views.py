"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""
import os
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
@app.route('/api/csrf-token', methods=['GET'])
def get_crsf():
    return jsonify({'csrf_token': generate_csrf()})

@app.route('/api/login', methods = ['POST'])#login function
def login():
    #form = LoginForm()
    #if form.validate_on_submit():
    #gets the data from the json
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = Users.query.filter_by(email=email).first() #search for user in the database
    if user is None: #checks if there's such a username
        #flash('Account does not exist, enter the correct username or <a href="/registration">create an account</a>.', 'warning')
        return jsonify({'success': False, 'message': 'Account does not exist'}), 404

    if user and user.check_password(password): #checks that the password is the one associated with that username
        login_user(user)
        return jsonify({'success': True}), 200

    return jsonify({'success': False, 'message': 'Incorrect password'}), 401 #for all times where password is incorrect but there is a user
    
        

@app.route('/api/registration', methods=['POST'])
def registration():#registration function
    #form = RegistrationForm

    #if form.validate_on_submit()

    #return redirect(url_for('index'))
    data = request.get_json() #get the data from the json
    if not data:
        return jsonify({"success": False, "message": "No JSON received"}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirmpassword = data.get('confirmpassword')

    user = Users.query.filter_by(username=username).first()
    emailcheck = Users.query.filter_by(email=email).first()
    if user is None: #making sure that there is no other user with the same name
        #create a user
        if password != confirmpassword:#makes sure the password confirmations match
            return jsonify({'success': False, 'message': 'Passwords must match'})
        if emailcheck: #check if there's an existing account with this email
            return jsonify({'success': False, 'message': 'Email already in use'})
        
        newuser = Users(#creates a user for this user
            username = username,
            email = email,
            password = password,
        )

        current_user.latitude = data['latitude']
        current_user.longitude = data['longitude']
        
        db.session.add(newuser) #adds user to database
        db.session.commit() #saves user

        login_user(newuser) #logs user in right after
        return jsonify({'success': True, 'message': 'User created'})
        
    else:
        return jsonify({'success': False, 'message': 'User already exists'})

@app.route('/api/profile', methods=['POST'])
def createProfile():#registration function
    #form = RegistrationForm

    #if form.validate_on_submit()

    #return redirect(url_for('index'))
    data = request.get_json() #get the data from the json
    if not data:
        return jsonify({"success": False, "message": "No JSON received"}), 400

    name = data.get('name')
    age = data.get('age')
    location = data.get('location')
    relationship = data.get('relationship')
    bio = data.get('bio')
    occupation = data.get('occupation')
    photo = data.get('location')
    filename = secure_filename(photo.filename)
    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    
    user_profile = Profile(#creates a user for this user
        user_id = current_user.id,
        name = name,
        age = age,
        location = location,
        relationship = relationship,
        bio = bio,
        occupation = occupation,
        photo = filename
    )

        
    db.session.add(user_profile) #adds user to database
    db.session.commit() #saves user

    #logs user in right after
    return jsonify({'success': True, 'message': 'Profile Updated'})
        


@app.route('/api/logout')
@login_required
def logout(): #logout function
    logout_user(current_user)#logs out the user
    return jsonify({'success': True, 'message': 'User Logged Out'})

@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(Users).filter_by(id=id)).scalar()

@app.route('/api/updatelocation', methods=['POST'])
def updateLocation():
    # Extracts JSON data from Request Body
    data = request.get_json()

    # Assigns coordinate values from the Request data
    current_user.latitude = data['latitude']
    current_user.longitude = data['longitude']

    # Enters value into the Database
    db.session.commit()

    return jsonify({'message' : "Location Updated"})

@app.route('/api/matches', methods=['GET'])
def getPotentialMatches():
    # Calculates the Total distance in km, using the current_user's and other user's longitude and latitude
    # Then Joins the preferences table to get the users radius from preferences
    # Allows the distance calculation from a specific table be a sub query 
    # Gets the users who radius falls within your range and you within their range
    query = text("""SELECT * FROM
                            (SELECT u.*,
                            (6307 * acos
                                (cos(radians(:lat1)) * cos(radians(u.latitude)) * 
                                cos(radians(u.longitude) - radians(:lon1)) + 
                                sin(radians(:lat1)) * sin(radians(u.latitude))
                    )) AS distance
                    FROM user u
                    JOIN preference p ON u.id = p.user_id
                ) AS sub
                WHERE distance <= :my_radius
                AND distance <= sub.radius
                """)
    # Runs and Executes SQL query and supplies values for SQL placeholders e.g(lat1) and returns all rows
    results = db.session.execute(query,{
        'lat1' : current_user.latitude,
        'lon1' : current_user.longitude,
        'myradius' : current_user.preference.radius
        }).fetchall()
    return jsonify(dict(user) for user in results)

@app.route('/api/interact', methods=['POST']) 
def Interaction():
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
    return jsonify({'message': "Interaction Complete"})

@app.route('/api/interact', methods=['GET'])
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

def checkMutualConnections(user1, user2):
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


@app.route('/api/favorite', methods=['POST'])
def add_favourite():
    # Retrieve data from json body
    data = request.get_json()

    # Creates a group of the User who favourtied and user who is being favourited
    fav = Favorite(
        user_id=current_user.id,
        favorite_id= data['user_id']
    )
    # Add the favourited user to the database
    db.session.add(fav)
    db.session.commit()

    return jsonify({'messsage': 'Successfully Added Favourties'})

@app.route('/api/favorites', methods=['GET'])
def get_favorties():
    favorite = db.session.query(Users).join(Favorite, Users.id == Favorite.favorite_id).filter(
        Favorite.user_id == current_user.id
        ).all()
    f_lst = [
        {
            'id': f.id,
            'username': f.username,
            'age': f.age
        } for f in favorite
    ]
    return jsonify({'favourite': f_lst})


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
        
@app.route('/api/getChat', methods=['GET'])
def get_chat():
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

@app.route('/api/message', methods=['POST'])
def send_message():
    # Retrieve data from json body
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

@app.route('/api/message/<int:chatroom_id>', methods=['GET'])
def get_message(chatroom_id):
    # Creates messages for a chatroom based url room selected and order each message accordingly 
    messages = Chat.query.filter_by(
        chatroom_id = chatroom_id
    ).order_by(Chat.timestamp.asc()).all()

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
def search():
    #Collect all the data from the urls from the frontend
    age_min = request.args.get('age_min', type=int)
    age_max = request.args.get('age_max', type=int)
    interest = request.args.get('interest')
    use_distance = request.args.get('radius', type=float)
    matches = request.args.get('matches', type=bool)
    sort = request.args.get('sort')
    # Creates a query for the User's table
    search_query = Users.query

    distance = 6371 * func.acos(
        func.cos(func.radians(current_user.latitude)) *
        func.cos(func.radians(Users.latitude)) *
        func.cos(func.radians(Users.longitude) - func.radians(current_user.longitude)) +
        func.sin(func.radians(current_user.latitude)) *
        func.sin(func.radians(Users.latitude))
    )

    # Checks if the url contains a max and min age and then filters the table based on the age
    if age_min and age_max:
        search_query = search_query.filter(Users.age.between(age_min,age_max))
    # Checks if the url contains an interest then checks userIDs that are associated with the interest ID then display those users
    if interest:
        search_query = search_query.join(UserInterests).join(Interest).filter(Interest.name == interest)
    # Checks if the url contains a match and gets the matched Ids from the matchMade function and filters the user table based on those matched Ids
    if matches:
        match_id = [m['user_id'] for m in matchMade()]
        search_query = search_query.filter(Users.id.in_(match_id))
    if use_distance:
        radius = current_user.preference.radius
        search_query = search_query.add_column(distance.label('distance')).filter(
            distance <= radius
        )
    
    # Apply Sorting on Search
    if sort =='newest':
        search_query = search_query.order_by(Users.id.asc())
    elif sort == 'oldest':
        search_query = search_query.order_by(Users.id.desc())
    
    # Gets a list of the query results and stores and displays the results using the user credentials
    s_result = search_query.all()
    result = [{
        "id": user.id,
        "username": user.username,
        "age": user.age
    } for user in s_result]

    return jsonify({'result': result}),200
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