from . import main_blueprint
from flask import render_template, request, redirect, url_for, current_app
from flask_restful import Api, Resource, url_for

# @main_blueprint.route('/')
# def index():

#     current_app.logger.info("Index page lading")
#     return {
#       "message":"SomeMessage"
#     }

api = Api(main_blueprint)

class Main(Resource):
  def get(self):
    return {
      'message':'Some message'
    }
  

api.add_resource(Main, '/main')