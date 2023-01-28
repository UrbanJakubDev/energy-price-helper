import io
import re
import zipfile
import pandas as pd
import docx
import os
import sys

from app.utils import docx_replace_regex
from docx2pdf import convert


# Get parent directory of current file
current_path_rel = os.path.dirname(os.path.realpath(__file__))
for k in range(2):
    current_path_rel = os.path.dirname(current_path_rel)

# Add parent directory to path
sys.path.append(current_path_rel)




'''

# Main parrent Class for generate statements from processed data
'''


class StatementGenerator():

    # Initialize class
    def __init__(self, input_file):
        self.input_file = input_file
        self.validated_file = None

        # TODO: Fix template path
        self.current_path_rel = current_path_rel
        self.tmp_directory =  self.current_path_rel +'/TMP_FOLDER/'
        self.template_docx = f'{self.tmp_directory}Statement_template.docx'
        self.storage = StatementStorage()
        

    # Generate statements

    def generate_statements(self):

        # Process input file and get validated data
        fp = InputFileProcessor(self.input_file)
        self.validated_file = fp.get_validated_data()

        print('Generating statements')
        print(self.validated_file)

        # Generate statements
        # Iterate through the rows of the dataframe and generate a PDF for each row
        for index, row in self.validated_file.iterrows():

            # Generate statement
            statement = self.generate_statement_file(row)
            # Convert statement to pdf

            # Save statement to directory
            statement.save(self.tmp_directory + str(row['id']) + '.docx')
           

        for file in os.listdir(self.tmp_directory):
            if file.endswith('.docx'):
                convert(self.tmp_directory + file, self.tmp_directory + file.replace('.docx', '.pdf'))
        
        

        respo = self.storage.zip_directory(directory_path=self.tmp_directory, zip_file_name='Statements.zip')

        # Return zip file from storage
        return respo

    # Generate single statement file

    def generate_statement_file(self, row):

        # TODO: Fix regex array
        # Create regex array for replacing placeholders in docx file
        regex_array = {
            'id': str(row['id']),
            'name': row['name'],
            'num1': str(row['num1']),
            'num2': str(row['num2']),
            'num3': str(row['num3']),
            'num4': str(row['num4']),
            'num5': str(row['num5'])
        }

        # Initialize DocxFiller class
        docx_filler = DocxFiller(self.template_docx)

        # Set regex array
        docx_filler.setRegexArray(regex_array)

        generated_file = docx_filler.replace_placeholders()
        return generated_file


class InputFileProcessor:
    def __init__(self, source_file):
        self.dataframe = pd.read_excel(source_file)

    def validate(self):
        """Validates the file"""
        # Add validation logic here
        print('Validating file')

    def calculations(self):
        """Make some calculations on the dataframe"""
        # Add calculation logic here
        print('Calculating')

    def get_validated_data(self):
        """Iterates through the rows of the dataframe and generates a PDF for each row"""
        print('Processing data')

        # Validate file
        self.validate()

        # Make calculations
        self.calculations()

        # Return validated data
        return self.dataframe


# Class for storing the generated statements, zip them and send them to the client
class StatementStorage():

    # Initialize class and create empty array for storing statements objects with id
    def __init__(self):
        self.statements = []

    # Add statement to storage
    def add_to_storage(self, statement, id):
        self.statements.append({
            'id': id,
            'statement': statement
        })

    # Load statements from storage and save them to folder
    def dump_from_storage(self, to_dir):
        print('Dumping statements')

        # Iterate through statements
        for statement in self.statements:

            # Save statement to folder
            statement['statement'].save(to_dir + str(statement['id']) + '.docx')

    # Zip method from ChatGPT

    def zip_directory(self, directory_path, zip_file_name):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path)
        zip_buffer.seek(0)
        return zip_buffer.read()

    # Clear storage folder and array

    def clear_storage(self, dir):
        self.statements = []

        # Delete all files in folder
        for file in os.listdir(dir):
            if file.endswith('.docx') and file.endswith('.zip') and '_template' not in file:
                os.remove(dir + file)

# Docx teplate file placeholder service
class DocxFiller():

    def __init__(self, file):
        self.doc = self.open_docx(file)
        self.regex_array = {}

    # Open document file-like object
    def open_docx(self, file):
        return docx.Document(open(file, 'rb'))

    def setRegexArray(self, regex_array):
        self.regex_array = regex_array

    # Replace regexes in docx file
    def replace_placeholders(self):
        document = self.doc

        for key, item in self.regex_array.items():
            key = re.compile(key)
            docx_replace_regex(document, key, item)

        return document


# Class for file
class File():

    def __init__(self, file):
        self.file = file
        self.file_name = self.file.filename
        self.file_extension = self.file_name.split('.')[-1]
        self.file_path = None

    # Save file to folder
    def save_file(self, to_dir):
        self.file_path = to_dir + self.file_name + '.' + self.file_extension
        self.file.save(self.file_path)

    # Delete file from folder
    def delete_file(self):
        os.remove(self.file_path)

    # Get file path
    def get_file_path(self):
        return self.file_path

    # Get file name
    def get_file_name(self):
        return self.file_name

    # Get file extension
    def get_file_extension(self):
        return self.file_extension

    # Get file
    def get_file(self):
        return self.file

    # Covert file to pdf
    def convert_to_pdf(self):

        if self.file_extension == 'docx':
            convert(self.file_path, self.file_path + '.pdf')