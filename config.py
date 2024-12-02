import os

class Config:
    SECRET_KEY = os.getenv ("SECRET_KEY", "your-secret-key")  # You can set a more secure secret key
    SQLALCHEMY_DATABASE_URI = os.getenv ("DATABASE_URL", "sqlite:///transportation.db")  # Can be switched to any other DB URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")  # Set a secure secret key for JWT
