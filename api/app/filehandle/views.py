import time
from . import file_blueprint
import os
from flask_restful import Api, Resource
from flask import Flask, request, jsonify, Response

# Import from services.py
from app.filehandle.services import StatementGenerator


# Initialize blueprint
api = Api(file_blueprint)


# Allowed file extensions array
ALLOWED_EXTENSIONS = set(['xlsx'])


# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# RREST API resource class
class FileResource(Resource):

    # TODO: only for testing
    def get(self):

        # Get path to file
        current_pah = os.path.dirname(os.path.abspath(__file__))

        # Get path to parent directory
        parent_dir = os.path.dirname(current_pah)

        current_path_rel = os.path.dirname(os.path.realpath(__file__))
        for k in range(1):
            current_path_rel = os.path.dirname(current_path_rel)

        return {
            'message': 'Here is you file..',
            'path': current_pah,
            'parent': parent_dir,
            'rel': current_path_rel
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

        # If validation is successful, save the file
        if file and allowed_file(file.filename):

            # Start timer
            start = time.time()
            proccesor = StatementGenerator(file)
            output_zip_file = proccesor.generate_statements()
       

            end = time.time()

            print('Time taken: ' + str(end - start))


            # Return 201 and message
            resp = jsonify({
                'message': 'File successfully uploaded', 
                'file': output_zip_file, 
                'fileName': proccesor.zip_file_name})
            resp.status_code = 201
            return resp

        else:
            resp = jsonify(
                {'message': 'Allowed file types are xls, xlsx, csv'})
            resp.status_code = 400
            return resp


api.add_resource(FileResource, '/file')
