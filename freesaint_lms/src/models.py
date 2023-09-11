from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class App_User(db.Model):
    __tablename__ = 'app_users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    googleid = db.Column(db.String(128), unique=True)
    gwttoken = db.Column(db.String(128), unique=True)
    profile_active = db.Column(db.Boolean)
    calculated_cal_goal = db.Column(db.Integer)
    starting_weight = db.Column(db.Integer)
    target_weight = db.Column(db.Integer)
    avatar_photo = db.Column(db.JSON)
    target_weight = db.Column(db.Integer)
    age = db.Column(db.Integer)
    height = db.Column(db.Integer)

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }


    # app_user to lms_login 1 to 1
#  user_id = db.Column(db.Integer, db.ForeignKey('users.id', nullable=False)) # 1-to-many
# lms_login to lms_permissions 1-to-many
# lms_chatgpt_sources to lms_courses 1-to-many

class LMS_Login (db.Model):
    __tablename__ = 'lms_logins'
    login_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(280), nullable=False)
    password = db.Column(db.String(280), nullable=False)
   

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def serialize(self):
        return {
            'id': self.username,
            'created_at': self.created_at.isoformat(),
        }


class LMS_Course (db.Model):
    __tablename__ = 'lms_courses'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(280), nullable=False)
    course_type = db.Column(db.String(280), nullable=False)
    course_description = db.Column(db.String(280))
    completed = db.Column(db.Boolean, nullable=False)
    quizzes = db.Column(db.String(280))

    def __init__(self, course_id: int, course_name: str):
        self.course_id = course_id
        self.course_name = course_name

    def serialize(self):
        return {
            'id': self.course_id,
            'created_at': self.created_at.isoformat(),
            'course_name': self.course_name
        }
    

# many-to-many bridge table lms_courses and lms_permissions
# many-to-many bridge table lms_courses and lms_quizzes
# many-to-many bridge table lms_chatgpt_sources and lms_topics
"""
likes_table = db.Table(
    'likes',
    db.Column(
        'user_id', db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),
    db.Column(
        'tweet_id', db.Integer,
        db.ForeignKey('tweets.id'),
        primary_key=True
    ),
    db.Column(
        'created_at', db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
)
"""
class LMS_Permission (db.Model):
    __tablename__ = 'lms_permissions'
    permission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    permission_name = db.Column(db.String(280), nullable=False)
    permission_module = db.Column(db.String(280), nullable=False, unique=True)

    def __init__(self, permission_id: int, permission_name: str):
        self.permission_id = permission_id
        self.permission_name = permission_name

    def serialize(self):
        return {
            'id': self.permission_id,
            'created_at': self.created_at.isoformat(),
            'permission_name': self.permission_name
        }


class LMS_ChatGPT_Source (db.Model):
    __tablename__ = 'lms_chatgpt_sources'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    podcast_transcripts = db.Column(db.String(280), nullable=False)
    youtube_transcripts= db.Column(db.String(280), nullable=False)
    health_blogs = db.Column(db.String(280), nullable=False)
    health_wikis = db.Column(db.String(280), nullable=False)
    health_book_libraries = db.Column(db.String(280), nullable=False)
    health_web_scrapes= db.Column(db.String(280), nullable=False)
    recipes = db.Column(db.String(280), nullable=False)

    def __init__(self, id: int):
        self.id = id

    def serialize(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat()
        }


class LMS_Topic (db.Model):
    __tablename__ = 'lms_topics'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gut_health = db.Column(db.String(280), nullable=False)
    hormones = db.Column(db.String(280), nullable=False)
    weight_loss = db.Column(db.String(280), nullable=False)
    mommy_makeover = db.Column(db.String(280), nullable=False)
    vegan = db.Column(db.String(280), nullable=False)
    keto = db.Column(db.String(280), nullable=False)
    pescatarian = db.Column(db.String(280), nullable=False)
    vegetarian = db.Column(db.String(280), nullable=False)
    intermittent_fasting = db.Column(db.String(280), nullable=False)
    nutrition = db.Column(db.String(280), nullable=False)
    cardio = db.Column(db.String(280), nullable=False)
    habits_motivation = db.Column(db.String(280), nullable=False)
    neuroscience_food = db.Column(db.String(280), nullable=False)
    loa_manifesting = db.Column(db.String(280), nullable=False)
    selfcare_sleep_stress = db.Column(db.String(280), nullable=False)
    vagus_nerve = db.Column(db.String(280), nullable=False)
    meditation = db.Column(db.String(280), nullable=False)
    yoga = db.Column(db.String(280), nullable=False)
    pilates = db.Column(db.String(280), nullable=False)
    nature = db.Column(db.String(280), nullable=False)
    weight_lifting = db.Column(db.String(280), nullable=False)
    hiits = db.Column(db.String(280), nullable=False)

    def __init__(self, id: int):
        self.id = id

    def serialize(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat()
        }
    