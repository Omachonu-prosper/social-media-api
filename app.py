from api import create_app
from config import Config

app = create_app()
if __name__ == '__main__':
    if Config.APP_ENV.lower() == 'production':
        app.run()
    else:
        app.run(debug=True)