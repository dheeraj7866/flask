from flask import Flask
import logging
import random

app = Flask(__name__)

# Set up logging configuration to include the necessary levels
logging.basicConfig(level=logging.INFO)

@app.route('/')
def homepage():
    app.logger.info('INFO: Homepage accessed')
    
    # Simulate different log scenarios
    if random.choice([True, False]):
        app.logger.warning('WARNING: This is a simulated warning message')
    
    if random.choice([True, False]):
        app.logger.error('ERROR: This is a simulated error message')

    return "Hello, World! by Dheeraj Kumar - Logging various events for testing CloudWatch"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
#hi from ui branch
#hi from ui branch 2
#from fix branch
#from fix branch part 2
