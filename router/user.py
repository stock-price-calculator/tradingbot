
from flask import Blueprint, jsonify, current_app
from kiwoom import Kiwoom
import constants

user_bp = Blueprint('user', __name__)

# 라우트 등록
@user_bp.route('/user', methods=['GET'])
def get_user():
    my = current_app.config['MY_KIWOOM']

    # if not kiwoom:
    #     return jsonify(0)
    name = my.get_master_code_name(constants.SAMSUNG_CODE)

    if not name:
        return jsonify(0)
    else:
        return jsonify(name)


@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return jsonify({'user_id': user_id, 'name': 'John Doe'})
