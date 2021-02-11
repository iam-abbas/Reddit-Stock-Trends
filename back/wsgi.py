from server import app

from datetime import datetime

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()