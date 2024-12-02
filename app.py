from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from models import db, User, Trip
from datetime import datetime


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Ensure 'config.py' exists and is properly set up

    # Initialize Extensions
    db.init_app(app)
    JWTManager(app)

    with app.app_context():
        db.create_all()  # Create database tables if they don't already exist

    # Define Routes
    @app.route('/')
    def home():
        return "Flask app is working!"

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'customer')  # Default role to 'customer'

        if not username or not email or not password:
            return jsonify({"message": "Missing required fields"}), 400

        if role not in ['customer', 'driver']:
            return jsonify({"message": "Invalid role provided"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"message": "Email already registered"}), 400

        user = User(username=username, email=email, role=role)
        user.set_password(password)  # Assuming set_password hashes the password
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({"message": "Invalid credentials"}), 401

        access_token = create_access_token(identity={"id": user.id, "username": user.username})
        return jsonify({"access_token": access_token}), 200



    @app.route('/driver/status', methods=['POST'])
    def update_driver_status():
        data = request.get_json()
        user_id = data.get('user_id')
        is_online = data.get('is_online')

    # Find the user by ID
        user = User.query.get(user_id)
        if not user or user.role != 'driver':
            return jsonify({"message": "User not found or not a driver"}), 404

    # Update the status
        user.is_online = is_online
        db.session.commit()

        return jsonify({"message": "Driver status updated successfully"}), 200

    
    @app.route('/trips', methods=['POST'])
    def request_trip():
        data = request.get_json()
        customer_id = data.get('customer_id')
        driver_id = data.get('driver_id')  # Optional
        start_location = data.get('start_location')
        end_location = data.get('end_location')

        if not customer_id or not start_location or not end_location:
            return jsonify({"error": "Customer ID, start location, and end location are required"}), 400

        # Assign a driver if not provided
        if not driver_id:
            driver = User.query.filter_by(is_online=True, availability=True).first()
            if not driver:
                return jsonify({"error": "No available drivers at the moment"}), 404
            driver_id = driver.id

        trip = Trip(
            customer_id=customer_id,
            driver_id=driver_id,
            start_location=start_location,
            end_location=end_location,
            date_time=datetime.utcnow(),
            trip_status="pending"
        )

        # Update the assigned driver's availability to False
        driver = User.query.get(driver_id)
        driver.availability = False

        db.session.add(trip)
        db.session.commit()

        return jsonify({
            "message": "Trip requested successfully",
            "trip_id": trip.id,
            "driver_id": driver_id
        }), 201

    
    return app

# Ensure to run the app correctly
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
