#!/usr/bin/python3
"""Entry point — start the HBnB API.

Usage:
    python run.py                       # development (default)
    FLASK_CONFIG=config.ProductionConfig python run.py
"""

import os

from app import create_app

config_class = os.getenv('FLASK_CONFIG', 'config.DevelopmentConfig')

app = create_app(config_class)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.config.get('DEBUG', False))
