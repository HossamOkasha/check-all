from flask import Flask, jsonify, request, abort

from flaskr.db import setup_db, db


def create_app(test_config=None):
  # Create and Config the app
  app = Flask(__name__)
  setup_db(app)

  # Root
  @app.route('/')
  def index():
    return 'developed by hos'

  return app


app = create_app()

if __name__ == '__main__':
  app.run()