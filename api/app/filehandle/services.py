import io
import re
import zipfile
import pandas as pd
import docx
import os
import sys

from app.utils import docx_replace_regex


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
        self.tmp_directory = self.current_path_rel + '/TMP_FOLDER/'
        self.template_docx = f'{self.tmp_directory}Statement_template.docx'
        self.zip_file_name = 'Statements.zip'
        self.zip_file_path = self.tmp_directory + self.zip_file_name

    # Generate statements

    def generate_statements(self):

        # Clear TMP folder
        self.clear_storage(self.tmp_directory)

        # Process input file and get validated data
        fp = InputFileProcessor(self.input_file)
        self.validated_file = fp.get_validated_data()

        print('Generating statements')
        print(self.validated_file)
        self.validated_file.to_excel('test.xlsx')

        # Generate statements
        # Iterate through the rows of the dataframe and generate a PDF for each row
        for index, row in self.validated_file.iterrows():

            # Generate statement
            statement = self.generate_statement_file(row)
            # Convert statement to pdf

            # Save statement to directory
            statement.save(self.tmp_directory + str(row['eic']) + '.docx')

        self.zip_directory(directory_path=self.tmp_directory, zip_file_name= self.zip_file_path)

        # return response 201 with message 'File uploaded successfully'
        return self.zip_file_path


    # Generate single statement file

    def generate_statement_file(self, row):

        # TODO: Fix regex array
        # Create regex array for replacing placeholders in docx file
        regex_array = {
            '#_month': str(row['month']),
            '#_name': str(row['name']),
            '#_q1': str(row['q1']),
            '#_q2': str(row['q2']),
            '#_q3': str(row['q3']),
            '#_statement_1_b': str(row['statement_1_b']),
            '#_statement_1_c': str(row['statement_1_c']),
            '#_statement_2_b': str(row['statement_2_b']),
            '#_statement_2_c': str(row['statement_2_c']),
            '#_statement_3_b': str(row['statement_3_b']),
            '#_statement_3_c': str(row['statement_3_c']),
            '#_statement_4_b': str(row['statement_4_b']),
            '#_statement_4_c': str(row['statement_4_c']),
            '#_statement_5_b': str(row['statement_5_b']),
            '#_statement_5_c': str(row['statement_5_c']),
            '#_statement_6_b': str(row['statement_6_b']),
            '#_statement_6_c': str(row['statement_6_c']),
            '#_statement_7_b': str(row['statement_7_b']),
            '#_statement_7_c': str(row['statement_7_c']),
            '#_statement_8_b': str(row['statement_8_b']),
            '#_statement_8_c': str(row['statement_8_c']),
            '#_statement_9_b': str(row['statement_9_b']),
            '#_statement_9_c': str(row['statement_9_c']),
            '#_statement_10_b': str(row['statement_10_b']),
            '#_statement_10_c': str(row['statement_10_c']),
            '#_statement_11_b': str(row['statement_11_b']),
            '#_statement_11_c': str(row['statement_11_c']),
            '#_statement_12_b': str(row['statement_12_b']),
            '#_statement_12_c': str(row['statement_12_c']),
            '#_statement_13_b': str(row['statement_13_b']),
            '#_statement_13_c': str(row['statement_13_c']),
            '#_calc_c': str(row['calculation_c']),
            '#_calc_d': str(row['calculation_d']),
            '#_calc_e': str(row['calculation_e'])
        }

        # Initialize DocxFiller class
        docx_filler = DocxFiller(self.template_docx)

        # Set regex array
        docx_filler.setRegexArray(regex_array)

        generated_file = docx_filler.replace_placeholders()
        return generated_file

    # Zip directory
    def zip_directory(self, directory_path, zip_file_name):

        # Create zip file
        zip_file = zipfile.ZipFile(zip_file_name, 'w')

        # Iterate over all the files in directory
        for folder, subfolders, files in os.walk(directory_path):
                
                for file in files:
                    # Create complete filepath of file in directory
                    file_path = os.path.join(folder, file)
                    if file.endswith('.docx') and '_template' not in file:
    
                        # Add file to zip file
                        zip_file.write(file_path, file, compress_type=zipfile.ZIP_DEFLATED)

        # Close the Zip File
        zip_file.close()


    # Clear storage folder and array
    def clear_storage(self, dir):

        # Delete all files in folder
        for file in os.listdir(dir):
            if file.endswith('.docx') and '_template' not in file:
                os.remove(dir + file)


class InputFileProcessor:
    def __init__(self, source_file):
        self.sf_sheetname = 'export'
        self.sf_header = 3  # Row number for header
        self.sf_usecols = 'A:K'  # Columns to use

        self.input_dataframe = pd.read_excel(
            source_file,
            sheet_name=self.sf_sheetname,
            header=self.sf_header,
            usecols=self.sf_usecols
        )

        self.output_dataframe = pd.DataFrame()

    def validate(self):
        """Validates the file"""
        # Add validation logic here
        print('Validating file')

    # Calculations on dataframe section

    @staticmethod
    def gj_to_mwh(gj):
        return round(gj * 0.277778, 3)

    @staticmethod
    def m3_to_mwh(m3):
        return round(m3/1000, 3)

    @staticmethod
    def kwh_to_mwh(kwh):
        return round(kwh * 0.001, 3)

    @staticmethod
    def calculation_c(num1, num5, num6, num8, num9, num12, num13):
        return (num9-num8)/num9*num6/num5*num1/(num1+num12+num13)*100

    @staticmethod
    def calculation_d(num1, num5, num6, num8, num9, num12, num13):
        return (num8/num9+(1-num8/num9)*(1-num6/num5)*(1-(num12+num13)/(num1+num12+num13)))*100

    @ staticmethod
    def calculation_e():
        pass

    def calculations(self):
        """Make some calculations on the dataframe"""

        # Copy base columns to output dataframe
        self.output_dataframe['name'] = self.input_dataframe['name']
        self.output_dataframe['month'] = self.input_dataframe['month']
        self.output_dataframe['eic'] = self.input_dataframe['eic']
        self.output_dataframe['statement_1_b'] = self.input_dataframe['gen_h_om']
        self.output_dataframe['statement_5_b'] = self.input_dataframe['sell_h_om']
        self.output_dataframe['statement_9_b'] = self.input_dataframe['cons_g_om']
        self.output_dataframe['statement_10_b'] = self.input_dataframe['gen_e_kj']


        # Calculations for base columns
        self.output_dataframe['statement_2_b'] = 0
        self.output_dataframe['statement_3_b'] = self.output_dataframe['statement_1_b'] - self.output_dataframe['statement_5_b']
        self.output_dataframe['statement_4_b'] = self.output_dataframe['statement_1_b'] - self.output_dataframe['statement_2_b'] - self.output_dataframe['statement_3_b'] - self.output_dataframe['statement_5_b']
        self.output_dataframe['statement_6_b'] = self.output_dataframe['statement_5_b']
        self.output_dataframe['statement_7_b'] = self.output_dataframe['statement_5_b'] - self.output_dataframe['statement_6_b']
        self.output_dataframe['statement_8_b'] = 0
        self.output_dataframe['statement_11_b'] = 0
        self.output_dataframe['statement_12_b'] = self.output_dataframe['statement_10_b']
        self.output_dataframe['statement_13_b'] = 0


        # Convert base columns to mwh
        self.output_dataframe['statement_1_c'] = self.output_dataframe['statement_1_b'].apply(self.gj_to_mwh)
        self.output_dataframe['statement_2_c'] = self.output_dataframe['statement_2_b'].apply(self.gj_to_mwh)
        self.output_dataframe['statement_3_c'] = self.output_dataframe['statement_3_b'].apply(self.gj_to_mwh)
        self.output_dataframe['statement_4_c'] = self.output_dataframe['statement_4_b'].apply(self.gj_to_mwh)
        self.output_dataframe['statement_5_c'] = self.output_dataframe['statement_5_b'].apply(self.gj_to_mwh)
        self.output_dataframe['statement_6_c'] = self.output_dataframe['statement_6_b'].apply(self.gj_to_mwh)
        self.output_dataframe['statement_7_c'] = self.output_dataframe['statement_7_b'].apply(self.gj_to_mwh)

        self.output_dataframe['statement_8_c'] = (self.output_dataframe['statement_8_b']*self.input_dataframe['combustion_heat']).apply(self.m3_to_mwh)
        self.output_dataframe['statement_9_c'] = (self.output_dataframe['statement_9_b']*self.input_dataframe['combustion_heat']).apply(self.m3_to_mwh)
        self.output_dataframe['statement_10_c'] = self.output_dataframe['statement_10_b'].apply(self.kwh_to_mwh)

        self.output_dataframe['statement_11_c'] = self.output_dataframe['statement_11_b'].apply(self.kwh_to_mwh)
        self.output_dataframe['statement_12_c'] = self.output_dataframe['statement_12_b'].apply(self.kwh_to_mwh)
        self.output_dataframe['statement_13_c'] = self.output_dataframe['statement_13_b'].apply(self.kwh_to_mwh)

        # Calculations 
        self.output_dataframe['calculation_c'] = self.calculation_c(
            num1=self.output_dataframe['statement_1_c'],
            num5=self.output_dataframe['statement_5_c'],
            num6=self.output_dataframe['statement_6_c'],
            num8=self.output_dataframe['statement_8_c'],
            num9=self.output_dataframe['statement_9_c'],
            num12=self.output_dataframe['statement_12_c'],
            num13=self.output_dataframe['statement_13_c']
        )

        self.output_dataframe['calculation_d'] = self.calculation_d(
            num1=self.output_dataframe['statement_1_c'],
            num5=self.output_dataframe['statement_5_c'],
            num6=self.output_dataframe['statement_6_c'],
            num8=self.output_dataframe['statement_8_c'],
            num9=self.output_dataframe['statement_9_c'],
            num12=self.output_dataframe['statement_12_c'],
            num13=self.output_dataframe['statement_13_c']
        )

        self.output_dataframe['calculation_e'] = 100 - self.output_dataframe['calculation_c'] - self.output_dataframe['calculation_d']

        # Questions
        self.output_dataframe['q1'] = self.input_dataframe['q1']
        self.output_dataframe['q2'] = self.input_dataframe['q2']
        self.output_dataframe['q3'] = self.input_dataframe['q3']

        self.output_dataframe = self.output_dataframe.round(2)



    def get_validated_data(self):
        """Iterates through the rows of the dataframe and generates a PDF for each row"""
        print('Processing data')

        # Validate file
        self.validate()

        # Make calculations
        self.calculations()

        # Return validated data
        return self.output_dataframe


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

