from flask import Flask
from flask_cors import CORS
from items.itemController import itemBp

app = Flask(__name__)
CORS(app)

app.register_blueprint(itemBp, url_prefix='/item')

@app.route('/')
def hello_world():
    return "flask mongodb atlas!"

if __name__ == "__main__":
    app.run(port=8000, debug=True)

