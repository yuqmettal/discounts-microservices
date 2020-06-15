import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APP_HOST = os.environ.get('APP_HOST', '127.0.0.1')
APP_PORT = os.environ.get('APP_PORT', 8081)

DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://discount_service:5b1c0d7be3c87c23e3d242a4cafd5889@localhost:5432/dev'
)

EUREKA_SERVER = os.environ.get('EUREKA_SERVER', 'http://localhost:8761/eureka')
