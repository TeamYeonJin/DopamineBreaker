import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CORS configuration
    CORS_HEADERS = 'Content-Type'
    _raw_cors_origins = os.environ.get(
        'CORS_ORIGINS',
        'http://localhost:3000,http://127.0.0.1:3000,'
        'http://localhost:5173,http://127.0.0.1:5173'
    )
    CORS_ORIGINS = [origin.strip() for origin in _raw_cors_origins.split(',') if origin.strip()]

class DevelopmentConfig(Config):
    """개발 환경 설정 - SQLite 사용"""
    DEBUG = True
    # SQLite 데이터베이스 사용 (간편한 개발용)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dopamine_breaker.db'
    SQLALCHEMY_ECHO = True  # SQL 쿼리 로그 출력

class ProductionConfig(Config):
    """프로덕션 환경 설정 - MySQL 사용"""
    DEBUG = False

    # MySQL 설정
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_PORT = os.environ.get('MYSQL_PORT') or 3306
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'dopamine_breaker'

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4'
    SQLALCHEMY_ECHO = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
