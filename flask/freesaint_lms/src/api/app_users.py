from flask import Blueprint, jsonify, abort, request
from ..models import LMS_Topic, App_User, LMS_Course, LMS_Login, LMS_Permission, LMS_Quiz, LMS_ChatGPT_Source, db

bp = Blueprint('app_users', __name__, url_prefix='/app_users')

@bp.route('', methods=['GET']) #DECORATOR TAKES PATH AND LIST OF HTTP VERBS
def index():
    app_users = App_User.query.all() # ORM performs SELECT query
    result = []
    for a in app_users:
        result.append(a.serialize()) # build list of App_Users as dictionaries
    return jsonify(result) # return JSON response

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    a = App_User.query.get_or_404(id, "App Users not found")
    return jsonify(a.serialize())

@bp.route('', methods=['POST'])
def create():
    #req body must contain id and name
    if 'id' not in request.json or 'name' not in request.json:
        return abort(400)
    #user with id of id must exist
    LMS_Login.query.get_or_404(request.json['Login_id'], "User not found")
    # construct App User
    a = App_User(
        id=request.json['id'],
        name=request.json['name']
    )
    db.session.add(a) #prepare CREATE statement
    db.session.commit() #execute CREATE statement
    return jsonify(a.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    a = App_User.query.get_or_404(id, "App User not found")
    try:
        db.session.delete(a)    # prepare DELETE statement
        db.session.commit()     # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
    
