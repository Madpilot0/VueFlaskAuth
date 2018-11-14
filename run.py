from flask import Flask, render_template, request, send_from_directory
from flask_cors import CORS
from backend.lib.Config import Config
from werkzeug.contrib.fixers import ProxyFix
from backend.routes.internal_routes import internal_routes
from time import time
import os

config = Config().getConfig()

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")

app.wsgi_app = ProxyFix(app.wsgi_app)
app.secret_key = config["server"]["appKey"] + str(int(time()))
cors = CORS(app, resources={r"/internal_routes/v1/*": {"origins": "*"}})
app.register_blueprint(internal_routes, url_prefix="/internal_routes/v1")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

# Uncomment the next files when favicons are added....
# @app.route('/assets/images/favicons/<icon>')
# def favicons(icon):
#   return send_from_directory(os.path.join(app.root_path, 'dist/assets/images/favicons'), icon)

# @app.route('/favicon.ico')
# def favicon():
#   return send_from_directory(os.path.join(app.root_path, 'dist/assets/images/favicons'), 'favicon.ico')

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=5001,debug=True)