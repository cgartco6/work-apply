import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///jobapp.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # PayFast Configuration
    PAYFAST_MERCHANT_ID = os.getenv('PAYFAST_MERCHANT_ID', '10000100')
    PAYFAST_MERCHANT_KEY = os.getenv('PAYFAST_MERCHANT_KEY', '46f0cd694581a')
    PAYFAST_URL = os.getenv('PAYFAST_URL', 'https://sandbox.payfast.co.za/eng/process')
    PAYFAST_RETURN_URL = os.getenv('PAYFAST_RETURN_URL', 'http://localhost:3000/payment/success')
    PAYFAST_CANCEL_URL = os.getenv('PAYFAST_CANCEL_URL', 'http://localhost:3000/payment/cancel')
    PAYFAST_NOTIFY_URL = os.getenv('PAYFAST_NOTIFY_URL', 'http://localhost:5000/api/payments/notify')
    
    # Application Configuration
    SERVICE_FEE = 499.00
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    @staticmethod
    def init_app(app):
        # Ensure upload directory exists
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    
    # Use PostgreSQL in production
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    # Strong secret keys for production
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
