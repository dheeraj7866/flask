from flask import Flask, request, jsonify
import logging
import random

app = Flask(__name__)

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Sample endpoint that randomly generates different types of logs
@app.route('/')
def hello():
    logger.info("INFO: Homepage accessed")
    return "Hello, World! by dheeraj kumar testing 123"

@app.route('/process')
def process():
    user_id = request.args.get("user_id", "unknown")
    # Simulate various log types based on random choice
    event_type = random.choice(['success', 'warning', 'error', 'info'])
    
    if event_type == 'success':
        logger.info(f"SUCCESS: Processed request for user {user_id}")
        return jsonify({"status": "success", "message": f"Processed user {user_id}"}), 200
    
    elif event_type == 'warning':
        logger.warning(f"WARNING: Potential issue with request from user {user_id}")
        return jsonify({"status": "warning", "message": "Potential issue detected"}), 200
    
    elif event_type == 'error':
        logger.error(f"ERROR: Failed processing request for user {user_id}")
        return jsonify({"status": "error", "message": "Processing failed"}), 500
    
    elif event_type == 'info':
        logger.info(f"INFO: Request received from user {user_id}")
        return jsonify({"status": "info", "message": "Request is being processed"}), 200

@app.errorhandler(404)
def not_found(error):
    logger.error(f"ERROR 404: Resource not found - {request.url}")
    return jsonify({"status": "error", "message": "Resource not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
