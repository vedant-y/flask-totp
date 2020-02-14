from flask import Blueprint, jsonify

from extensions.flask_totp import totp_required

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify(message = "¯\\_(ツ)_/¯")

@main.route('/jony-ive')
@totp_required
def jony_ive():
    return jsonify(message = "Aluminium!")

@main.route('/scott-forstall')
def scott_forstall():
    return jsonify(message = "Skeuomorphism!")
