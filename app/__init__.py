from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')

