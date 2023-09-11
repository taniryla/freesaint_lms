from flask import Blueprint, jsonify, abort, request
from ..models import LMS_Topic, App_User, LMS_Course, LMS_Login, LMS_Permission, LMS_Quiz, LMS_ChatGPT_Source, db
import hashlib
import secrets

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


bp = Blueprint('lms_logins', __name__, url_prefix='/lms_logins')

@bp.route('', methods=['GET']) #DECORATOR TAKES PATH AND LIST OF HTTP VERBS
def index():
    lms_logins = LMS_Login.query.all() # ORM performs SELECT query
    result = []
    for l in lms_logins:
        result.append(l.serialize()) # build list of LMS_Logins as dictionaries
    return jsonify(result) # return JSON response

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    l = LMS_Login.query.get_or_404(id, "LMS Login not found")
    return jsonify(l.serialize())

@bp.route('', methods=['POST'])
def create():
    #req body must contain login_id and username
    if 'login_id' not in request.json or 'username' not in request.json:
        return abort(400)
    #user with id of login_id must exist
    App_User.query.get_or_404(request.json['id'], "User not found")
    # construct LMS Logins
    l = LMS_Login(
        login_id=request.json['login_id'],
        username=request.json['username']
    )
    db.session.add(l) #prepare CREATE statement
    db.session.commit() #execute CREATE statement
    return jsonify(l.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(login_id: int):
    l = LMS_Login.query.get_or_404(login_id, "Login not found")
    try:
        db.session.delete(l)    # prepare DELETE statement
        db.session.commit()     # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)