# run.py
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    host = os.getenv('FLASK_RUN_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_RUN_PORT', 5000))
    debug_mode = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'

    app.run(host=host, port=port, debug=debug_mode)
