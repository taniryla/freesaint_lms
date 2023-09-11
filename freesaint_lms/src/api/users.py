from flask import Blueprint, jsonify, abort, request
from ..models import User, db, Tweet, likes_table
import hashlib
import secrets

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('', methods=['GET']) #DECORATOR TAKES PATH AND LIST OF HTTP VERBS
def index():
    users = User.query.all() # ORM performs SELECT query
    result = []
    for u in users:
        result.append(u.serialize()) # build list of Users as dictionaries
    return jsonify(result) # return JSON response

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    u = User.query.get_or_404(id, "User not found")
    return jsonify(u.serialize())

@bp.route('', methods=['POST'])
def create():
    #req body must contain user_id and content
    if 'username' not in request.json or 'password' not in request.json:
        return abort(400)
    if len(request.json['username']) <= 3 or len(request.json['password']) <= 8:
        return abort(400)
    # construct User
    u = User(
        username=request.json['username'],
        password=scramble(request.json['password'])
    )
    db.session.add(u) #prepare CREATE statement
    db.session.commit() #execute CREATE statement
    return jsonify(u.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    u = User.query.get_or_404(id, "User not found")
    try:
        db.session.delete(u)    # prepare DELETE statement
        db.session.commit()     # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
    
@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    u = User.query.get_or_404(id) # this code queries the user table to find out if a user record with the requested id exists
     #req body must contain username only, password only and both username and password
    if 'username' not in request.json or 'password' not in request.json:
        return abort(400)
    if len(request.json['username']) <= 3 or len(request.json['password']) <= 8:
        return abort(400)
    # construct User
    u = User(
        username=request.json['username'],
        password=scramble(request.json['password'])
    )
    try:
        db.session.update(u)    # prepare UPDATE statement
        db.session.commit()     # execute UPDATE statement
        return jsonify(u.serialize())
    except:
        # something went wrong :(
        return jsonify(False)
    
@bp.route('/<int:id>/liking_tweets', methods=['GET'])
def liking_tweets(id: int):
    u = User.query.get_or_404(id)
    result = []
    for t in u.liking_tweets:
        result.append(t.serialize())
    return jsonify(result)