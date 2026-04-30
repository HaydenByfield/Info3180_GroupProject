"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""
import os
from app import app, db
from flask import render_template, request, jsonify, send_file
from flask_login import current_user
from sqlalchemy import text, func
from app.models import Interactions, Users, Preferences, UserInterests, Interest, Favorite


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

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
            # Create a list of matched users for the current_user
            matches.append({
                'user_id': i.to_user
            })
    return jsonify(matches), 200

@app.route('/api/checkmatch')
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