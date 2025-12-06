#!/usr/bin/env python3
import sys
import traceback
sys.path.insert(0, '/Users/aariyagage/DatabaseProject/backend')
try:
    from app import app
    if __name__ == '__main__':
        app.run(debug=False, port=5000, host='127.0.0.1')
except Exception as e:
    print(f"Error starting app: {e}")
    traceback.print_exc()
