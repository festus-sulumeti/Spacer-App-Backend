from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from datetime import timedelta
from models import db, User, Space, Booking
from config import DATABASE_CONFIG  # Import the config
import secrets

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['pw']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['db']}"

# Generate a random secret key
jwt_secret_key = secrets.token_hex(32)  # Generate a 32-byte (256-bit) random key

# Set the JWT_SECRET_KEY in your Flask app's configuration
app.config['JWT_SECRET_KEY'] = jwt_secret_key

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# URL Routing
@app.route('/')
def index():
    return "This is a basic Flask application"

# Admin Login Route with JWT Authentication
@app.route('/adminlogin', methods=['POST'])
def admin_login():
    data = request.get_json()

    # Check login credentials
    if data['email'] == 'admin@gmail.com' and data['password'] == 'password':
        expiration_time = timedelta(hours=1)
        token = create_access_token(identity=data['email'], expires_delta=expiration_time)

        return jsonify({"success": True, "message": "Login successful", "token": token, 'user_email': data['email'], 'role': 'admin'}), 200
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401


# Route for admin logout
@app.route('/adminlogout', methods=['POST'])
#@jwt_required()  # Protect this route with JWT authentication
def admin_logout():
    try:
        # Unset JWT cookies to log the user out
        response = jsonify({"success": True, "message": "Logout successful"})
        unset_jwt_cookies(response)
        return response, 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# Add Space Route
@app.route('/spaces', methods=['POST'])
#@jwt_required()  # Protect this route with JWT authentication
def add_space():
    data = request.get_json()
    new_space = Space(name=data['name'], description=data['description'], location=data['location'], price_per_hour=data['price_per_hour'], owner_id=data['owner_id'])
    db.session.add(new_space)
    db.session.commit()
    return jsonify({"success": True, "message": "Space added successfully"}), 201

# View All Spaces Route
@app.route('/spaces', methods=['GET'])
def get_spaces():
    spaces = Space.query.all()
    space_list = []
    for space in spaces:
        space_data = {
            'id': space.id,
            'name': space.name,
            'description': space.description,
            'location': space.location,
            'price_per_hour': str(space.price_per_hour),  # Convert to string for JSON compatibility
            'owner_id': space.owner_id,
            'created_at': str(space.created_at)  # Convert to string for JSON compatibility
        }
        space_list.append(space_data)
    return jsonify({"success": True, "spaces": space_list}), 200

# URL Route for adding a new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    # Hash the password before storing it in the database
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"success": True, "message": "User added successfully"}), 201

@app.route('/userlogin', methods=['POST'])
def user_login():
    data = request.get_json()

    # Check if the user exists
    user = User.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        expiration_time = timedelta(hours=1)
        token = create_access_token(identity=user.email, expires_delta=expiration_time)
        return jsonify({"success": True, "message": "Login successful", "token": token, 'user_email': user.email, 'role': user.role}), 200
    else:
        return jsonify({"success": False, "message": "Invalid email or password"}), 401
    
# URL Route for getting all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role  # Include 'role' in the response
        }
        user_list.append(user_data)
    return jsonify({"success": True, "users": user_list}), 200

@app.route('/userlogout', methods=['POST'])
#@jwt_required()  # Protect this route with JWT authentication
def user_logout():
    try:
        # Unset JWT cookies to log the user out
        response = jsonify({"success": True, "message": "Logout successful"})
        unset_jwt_cookies(response)
        return response, 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}),
    
# Add Booking Route
# @app.route('/bookings', methods=['POST'])
# def add_booking():
#     data = request.get_json()
#     new_booking = Booking(user_id=data['user_id'], space_id=data['space_id'], start_time=data['start_time'], end_time=data['end_time'], status=data.get('status', 'pending'), payment_status=data.get('payment_status', 'unpaid'))
#     db.session.add(new_booking)
#     db.session.commit()
#     return jsonify({"success": True, "message": "Booking added successfully"}), 201

# # View All Bookings Route
# @app.route('/bookings', methods=['GET'])
# def get_bookings():
    bookings = Booking.query.all()
    booking_list = []
    for booking in bookings:
        booking_data = {
            'id': booking.id,
            'user_id': booking.user_id,
            'space_id': booking.space_id,
            'start_time': str(booking.start_time),  # Convert to string for JSON compatibility
            'end_time': str(booking.end_time),  # Convert to string for JSON compatibility
            'status': booking.status,
            'payment_status': booking.payment_status,
            'created_at': str(booking.created_at)  # Convert to string for JSON compatibility
        }
        booking_list.append(booking_data)
    return jsonify({"success": True, "bookings": booking_list}), 200

# Add Booking Route
@app.route('/bookings', methods=['POST'])
# @jwt_required()  # Protect this route with JWT authentication
def add_booking():
    data = request.get_json()
    
    # user_id = get_jwt_identity()

    # Check if all required fields are present in the request
    required_fields = ['user_id', 'space_id', 'start_time', 'end_time']
    if not all(field in data for field in required_fields):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    # Validate start_time and end_time format
    try:
        start_time = datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M:%S')
        end_time = datetime.strptime(data['end_time'], '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return jsonify({"success": False, "message": "Invalid date/time format. Use ISO 8601 format: YYYY-MM-DDTHH:MM:SS"}), 400

    # Check if the space exists
    space = Space.query.get(data['space_id'])
    if not space:
        return jsonify({"success": False, "message": "Space not found"}), 404

    # Create and add the new booking
    new_booking = Booking(
        user_id=data['user_id'],
        space_id=data['space_id'],
        start_time=start_time,
        end_time=end_time,
        status=data.get('status', 'pending'),
        payment_status=data.get('payment_status', 'unpaid')
    )
    db.session.add(new_booking)
    db.session.commit()

    return jsonify({"success": True, "message": "Booking added successfully"}), 201

# Modify the get_bookings route to format the date/time strings
@app.route('/bookings', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    booking_list = []
    for booking in bookings:
        booking_data = {
            'id': booking.id,
            'user_id': booking.user_id,
            'space_id': booking.space_id,
            'start_time': booking.start_time.strftime('%Y-%m-%dT%H:%M:%S'),  # Format start_time
            'end_time': booking.end_time.strftime('%Y-%m-%dT%H:%M:%S'),  # Format end_time
            'status': booking.status,
            'payment_status': booking.payment_status,
            'created_at': booking.created_at.strftime('%Y-%m-%dT%H:%M:%S')  # Format created_at
        }
        booking_list.append(booking_data)
    return jsonify({"success": True, "bookings": booking_list}), 200


if __name__ == '__main__':
    app.run(debug=True)