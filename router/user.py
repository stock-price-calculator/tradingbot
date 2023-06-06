
from flask import Blueprint, jsonify

user_bp = Blueprint('user', __name__)

# 라우트 등록
@user_bp.route('/user', methods=['GET'])
def get_user():
    return jsonify({'message': 'User route'})

@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return jsonify({'user_id': user_id, 'name': 'John Doe'})
