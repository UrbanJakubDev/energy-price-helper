from . import file_blueprint
import os
from flask_restful import Api, Resource
from flask import Flask, request, jsonify, current_app

api = Api(file_blueprint)

ALLOWED_EXTENSIONS = set(['xlsx'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class FileResource(Resource):

    def get(self):
        return {
            'message': 'Here is you file..'
        }

    def post(self):
        # check if the post request has the file part
        if 'file' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp

        file = request.files['file']

        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp

        if file and allowed_file(file.filename):
            file.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'],'file.xlsx'))
            resp = jsonify({'message': 'File successfully uploaded'})
            resp.status_code = 201
            return resp

        else:
            resp = jsonify(
                {'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
            resp.status_code = 400
            return resp

api.add_resource(FileResource, '/file')
