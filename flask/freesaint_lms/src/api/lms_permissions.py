from flask import Blueprint, jsonify, abort, request
from ..models import LMS_Topic, App_User, LMS_Course, LMS_Login, LMS_Permission, LMS_Quiz, LMS_ChatGPT_Source, db
import hashlib
import secrets

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


bp = Blueprint('lms_permissions', __name__, url_prefix='/lms_permissions')

@bp.route('', methods=['GET']) #DECORATOR TAKES PATH AND LIST OF HTTP VERBS
def index():
    lms_permissions = LMS_Permission.query.all() # ORM performs SELECT query
    result = []
    for l in lms_permissions:
        result.append(l.serialize()) # build list of LMS_Permissions as dictionaries
    return jsonify(result) # return JSON response

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    l = LMS_Permission.query.get_or_404(id, "LMS Permission not found")
    return jsonify(l.serialize())

@bp.route('', methods=['POST'])
def create():
    #req body must contain permission_id and permission_name
    if 'permission_id' not in request.json or 'permission_name' not in request.json:
        return abort(400)
    #user with id of permission_id must exist
    App_User.query.get_or_404(request.json['id'], "User not found")
    # construct LMS Permissions
    l = LMS_Permission(
        permission_id=request.json['permission_id'],
        permission_name=request.json['permission_name']
    )
    db.session.add(l) #prepare CREATE statement
    db.session.commit() #execute CREATE statement
    return jsonify(l.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(permission_id: int):
    l = LMS_Quiz.query.get_or_404(permission_id, "Permission not found")
    try:
        db.session.delete(l)    # prepare DELETE statement
        db.session.commit()     # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
    
@bp.route('/<int:id>/courses_permissions', methods=['GET'])
def courses_permissions(id: int):
    l = LMS_Permission.query.get_or_404(id)
    result = []
    for u in l.courses_permissions:
        result.append(u.serialize())
    return jsonify(result)