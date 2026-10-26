from backend import app
from backend.routes import seed_database
if __name__ == '__main__':
    seed_database()
    app.run(host='0.0.0.0', port=8080)
