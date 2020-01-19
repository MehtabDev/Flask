from flask import Flask
from user import users
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required
# from geopy.geocoders import Nominatim


app = Flask(__name__)
jwt = JWTManager(app)
CORS(app)
#JWT CONFIG
app.config['JWT_SECRET_KEY'] = 'THIS_IS_A_SCRET_KEY'


def run_scheduler():
    print('Job running')


@app.route('/create/user', methods=['GET', 'POST'])
def register_user():
    return users.sign_up()


@app.route('/user/login', methods=['GET', 'POST'])
def login_user():
    return users.login()


@app.route("/user/profile", methods=['GET'])
@jwt_required # need to protect profile method, Authorization will automatically verify
def profile_user():
    return users.profile()


@app.route('/', methods=['GET'])
def check_url():
    return "running..."


if __name__ == '__main__':
    # result = Geocoder.reverse_geocode(31.3372728, -109.5609559, True)
    # geolocator = Nominatim(user_agent="Mehtbatesting")
    # result = geolocator.reverse("28.6210,77.3812")
    # result = geolocator.reverse("28.570327199999998, 77.283266099999999")
    # result = geolocator.reverse("28.570327199999998, 77.283266099999999")
    # print(result.raw)
    # app.run("localhost", debug=True)
    app.run(host='0.0.0.0')

