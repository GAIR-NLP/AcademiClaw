
import os

class Config:
    # System Configuration
    DEBUG = False
    UPLOAD_FOLDER = './uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    # Security Keys
    SECRET_KEY = "SK_LIVE_2024"
    DB_PASSWORD = "db_pass_complex_123"
