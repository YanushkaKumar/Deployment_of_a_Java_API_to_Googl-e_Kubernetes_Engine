from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)

# Single Colombo location data
COLOMBO_LOCATION = {
    'latitude': 7.4675,
    'longitude': 80.6234,
    'timestamp': datetime.now(timezone.utc).isoformat(),
    'accuracy': 15.5,

}

@app.route('/')
def home():
    """API home page"""
    return jsonify({
        'message': 'Simple Location Tracker API',
        'status': 'running',
        'location': 'Colombo, Sri Lanka'
    })

@app.route('/api/locations', methods=['GET'])
def get_locations():
    """Get Colombo location"""
    try:
        # Update timestamp to current time
        location = COLOMBO_LOCATION.copy()
        location['timestamp'] = datetime.now(timezone.utc).isoformat()
        
        return jsonify({
            'success': True,
            'count': 1,
            'locations': [location]
        })
    except Exception as e:
        print(f"❌ Error in get_locations: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'location_available': True
    })

if __name__ == '__main__':

    
    app.run(host='0.0.0.0', port=5000, debug=True)