from flask import Blueprint, jsonify, abort, request
from ..models import LMS_Topic, App_User, LMS_Course, LMS_Login, LMS_Permission, LMS_Quiz, LMS_ChatGPT_Source, db
import hashlib
import secrets

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


bp = Blueprint('lms_chatgpt_sources', __name__, url_prefix='/lms_chatgpt_sources')

@bp.route('', methods=['GET']) #DECORATOR TAKES PATH AND LIST OF HTTP VERBS
def index():
    lms_chatgpt_sources = LMS_ChatGPT_Source.query.all() # ORM performs SELECT query
    result = []
    for l in lms_chatgpt_sources:
        result.append(l.serialize()) # build list of LMS_ChatGPT_Sources as dictionaries
    return jsonify(result) # return JSON response

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    l = LMS_ChatGPT_Source.query.get_or_404(id, "LMS ChatGPT Sources not found")
    return jsonify(l.serialize())

@bp.route('', methods=['POST'])
def create():
    #req body must contain id 
    if 'id' not in request.json:
        return abort(400)
    #user with id of id must exist
    App_User.query.get_or_404(request.json['id'], "User not found")
    # construct LMS ChatGPT Sources
    l = LMS_ChatGPT_Source(
        id=request.json['id'],
    )
    db.session.add(l) #prepare CREATE statement
    db.session.commit() #execute CREATE statement
    return jsonify(l.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    l = LMS_ChatGPT_Source.query.get_or_404(id, "ChatGPT Source not found")
    try:
        db.session.delete(l)    # prepare DELETE statement
        db.session.commit()     # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
    
@bp.route('/<int:id>/chatgpt_sources_topics', methods=['GET'])
def chatgpt_sources_topics(id: int):
    l = LMS_ChatGPT_Source.query.get_or_404(id)
    result = []
    for u in l.chatgpt_sources_topics:
        result.append(u.serialize())
    return jsonify(result)