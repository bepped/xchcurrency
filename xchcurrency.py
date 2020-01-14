import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
if app.config['STARTUP_STATUS'] == 'NOK':
    app.logger.error(app.config['HTTP_ERROR'])

@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
