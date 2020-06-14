import os

DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://discount_service:5b1c0d7be3c87c23e3d242a4cafd5889@localhost:5432/dev'
)
