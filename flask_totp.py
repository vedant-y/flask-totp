from flask import current_app, jsonify, request
from functools import wraps
import pyotp

__version__ = '1.0.0'

__extension_key__ = 'FLASK_TOTP'
__secret_key__ = 'FLASK_TOTP_SECRET'

class FlaskTOTP(object):
    """
    Wrapper around PyOTP library for handling time-based OTP counters in a Flask environment.
    """
    def __init__(self, app=None):
        """
        :param app: optional Flask application object (defaults to None)
        """
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        :param app: the Flask application object
        :raises RuntimeError: if seed 'FLASK_TOTP_SECRET' is not provided in configuration
        """
        secret = app.config.get(__secret_key__)
        if secret is None:
            raise RuntimeError("{} not defined in configuration".format(__secret_key__))

        self.totp = pyotp.TOTP(secret)

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions[__extension_key__] = self

    def verify(self, token, for_time=None, valid_window=0):
        """
        Verifies the OTP passed in against the current time OTP.

        :param otp: the OTP to check against
        :param for_time: Time to check OTP at (defaults to now)
        :param valid_window: extends the validity to this many counter ticks before and after the current one
        :returns: True if verification succeeded, False otherwise
        """
        return self.totp.verify(token, for_time, valid_window)

def totp_required(f):
    """
    Decorates route to verify the OTP passed with authorization header against the current time OTP before chain proceeds.

        Request Header -> Authorization: TOTP 528941

    :returns: following view function if verification succeeded, else jsonify with message for failure
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header is not None:
            scheme, token = auth_header.split()

            flask_totp = current_app.extensions.get(__extension_key__)
            if flask_totp and scheme == 'TOTP' and flask_totp.verify(token) == True:
                return f(*args, **kwargs)

        return jsonify(message = "TOTP verification failed.")
    return decorated_function
