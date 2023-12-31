from flask import Blueprint, jsonify, abort, request
from ..models import LMS_Topic, App_User, LMS_Course, LMS_Login, LMS_Permission, LMS_Quiz, LMS_ChatGPT_Source, db
import hashlib
import secrets

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


bp = Blueprint('lms_quizzes', __name__, url_prefix='/lms_quizzes')

@bp.route('', methods=['GET']) #DECORATOR TAKES PATH AND LIST OF HTTP VERBS
def index():
    lms_quizzes = LMS_Quiz.query.all() # ORM performs SELECT query
    result = []
    for l in lms_quizzes:
        result.append(l.serialize()) # build list of LMS_Quizzes as dictionaries
    return jsonify(result) # return JSON response

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    l = LMS_Quiz.query.get_or_404(id, "LMS Quiz not found")
    return jsonify(l.serialize())

@bp.route('', methods=['POST'])
def create():
    #req body must contain quiz_id and quiz_name
    if 'quiz_id' not in request.json or 'quiz_name' not in request.json:
        return abort(400)
    #user with id of quiz_id must exist
    App_User.query.get_or_404(request.json['id'], "User not found")
    # construct LMS Quizzes
    l = LMS_Quiz(
        quiz_id=request.json['quiz_id'],
        quiz_name=request.json['quiz_name']
    )
    db.session.add(l) #prepare CREATE statement
    db.session.commit() #execute CREATE statement
    return jsonify(l.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(quiz_id: int):
    l = LMS_Quiz.query.get_or_404(quiz_id, "Quiz not found")
    try:
        db.session.delete(l)    # prepare DELETE statement
        db.session.commit()     # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
    
@bp.route('/<int:id>/courses_quizzes', methods=['GET'])
def courses_quizzes(id: int):
    l = LMS_Quiz.query.get_or_404(id)
    result = []
    for u in l.courses_quizzes:
        result.append(u.serialize())
    return jsonify(result)