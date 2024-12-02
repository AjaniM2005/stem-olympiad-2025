from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


# Initialize the db object
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Ensure password is hashed
    role = db.Column(db.String(50), nullable=False)  # 'customer' or 'driver'
    is_online = db.Column(db.Boolean, default=False)  # Used for taxi driver online/offline status
    availability = db.Column(db.Boolean, default=True)  # Driver availability
    
    # Method to set password (hashing it before saving)
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Method to check password
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'

    def check_available_driver():
        return User.query.filter_by(user_type="driver", availability=True).first()


class Trip(db.Model):
    __tablename__ = 'trips'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_location = db.Column(db.String(200), nullable=False)
    end_location = db.Column(db.String(200), nullable=False)
    trip_status = db.Column(db.String(50), default="pending")  # 'completed', 'cancelled', etc.
    date_time = db.Column(db.DateTime, nullable=False)

    customer = db.relationship('User', foreign_keys=[customer_id])
    driver = db.relationship('User', foreign_keys=[driver_id])

    def __repr__(self):
        return f'<Trip {self.id} from {self.start_location} to {self.end_location}>'
