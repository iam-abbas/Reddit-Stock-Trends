from server import app, ensure_data_exists

from datetime import datetime

def main():
    ensure_data_exists()
    app.run(host='0.0.0.0', port=5006)

if __name__ == '__main__':
    main()