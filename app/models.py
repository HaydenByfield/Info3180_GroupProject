from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class Users(db.Model):
    __tablename__ = 'user_profile'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(256), nullable = False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    preference = db.relationship('Preferences', backref='users', uselist=False)
    interest = db.relationship('Interest', secondary='user_interests_profile', backref='users')
    profile = db.relationship('Profile', backref='users')

    def __init__(self, username, first_name, last_name, age, password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(password, self.password)
    
    def is_authenticated():
        return True
    
    def is_active():
        return True
    
    def is_anonymus():
        return False
    
    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return(self.id)
        
    def __repr__(self):
        return '<user %r>' % (self.username)
    
class Profile(db.Model):
    __tablename__ = 'p_profile'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    name = db.Column(db.String(80), nullable = False)
    location = db.Column(db.String(80), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    Bio = db.Column(db.Text)
    relationship = db.Column(db.String(80), nullable = False)
    occupation = db.Column(db.String(80), nullable = False)
    photo = db.Column(db.String(80), nullable = False)



# Store User Preferences
class Preferences(db.Model):
    __tablename__ = 'preferences_profile'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    radius = db.Column(db.Float, nullable = False)
    min_age = db.Column(db.Integer)
    max_age = db.Column(db.Integer)

    def __self__(self, radius, min_age, max_age, interest, gender):
        self.radius = radius
        self.min_age = min_age
        self.max_age = max_age
        self.interest = interest
        self. gender = gender

    def __repr__(self):
        return '<Preferences %r>' % (self.range)
    
class Interest(db.Model):
    __tablename__ = 'interest_profile'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

class UserInterests(db.Model):
    __tablename__ = 'user_interests_profile'

    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), primary_key=True)
    interest_id = db.Column(db.Integer, db.ForeignKey('interest_profile.id'), primary_key=True)

#Store Ratings from user to user
class Interactions(db.Model):
    __tablename__ = 'interactions_profile'

    id = db.Column(db.Integer, primary_key = True)
    from_user = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    to_user = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    action = db.Column(db.String(80))
    
class Favorite(db.Model):
    __tablename__ = 'favourtie_profile'

    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    favorite_id = db.Column(db.Integer, primary_key=True)


class ChatRoom(db.Model):
    __tablename__ = 'chatroom_profile'

    id = db.Column(db.Integer, primary_key=True)
    chat1_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    chat2_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))

class Chat(db.Model):
    __tablename__ = 'chat_profile'

    id = db.Column(db.Integer, primary_key=True)
    chatroom_id = db.Column(db.Integer, db.ForeignKey('chatroom_profile.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    message = db.Column(db.Text)




    