from flask import Blueprint, jsonify, abort, request
from ..models import LMS_Topic, App_User, LMS_Course, LMS_Login, LMS_Permission, LMS_Quiz, LMS_ChatGPT_Source, db, courses_permissions, courses_quizzes
import hashlib
import secrets

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


bp = Blueprint('lms_courses', __name__, url_prefix='/lms_courses')

@bp.route('', methods=['GET']) #DECORATOR TAKES PATH AND LIST OF HTTP VERBS
def index():
    lms_courses = LMS_Course.query.all() # ORM performs SELECT query
    result = []
    for l in lms_courses:
        result.append(l.serialize()) # build list of LMS_Courses as dictionaries
    return jsonify(result) # return JSON response

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    l = LMS_Course.query.get_or_404(id, "LMS Course not found")
    return jsonify(l.serialize())

@bp.route('', methods=['POST'])
def create():
    #req body must contain course_id and course_name
    if 'course_id' not in request.json or 'course_name' not in request.json:
        return abort(400)
    #user with id of course_id must exist
    LMS_Permission.query.get_or_404(request.json['id'], "Permission not found")
    # construct LMS Courses
    l = LMS_Course(
    course_id=request.json['course_id'],
    course_name=request.json['course_name']
    )
    db.session.add(l) #prepare CREATE statement
    db.session.commit() #execute CREATE statement
    return jsonify(l.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(course_id: int):
    l = LMS_Course.query.get_or_404(course_id, "Course not found")
    try:
        db.session.delete(l)    # prepare DELETE statement
        db.session.commit()     # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
    
@bp.route('/<int:id>/courses_permissions', methods=['GET'])
def courses_permissions (id: int):
    l = LMS_Course.query.get_or_404(id)
    result = []
    for b in l.courses_permissions:
        result.append(b.serialize())
    return jsonify(result)

@bp.route('/<int:id>/courses_quizzes', methods=['GET'])
def courses_quizzes (quiz_id: int):
    l = LMS_Course.query.get_or_404(quiz_id)
    result = []
    for b in l.courses_quizzes:
        result.append(b.serialize())
    return jsonify(result)