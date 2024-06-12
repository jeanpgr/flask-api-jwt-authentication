import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'AI_SYSTEM24'
    # Otras configuraciones