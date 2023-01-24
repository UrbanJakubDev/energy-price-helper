
# '''
# Class for the processing of the file

# This class is responsible for the processing of the file
# Processing includes:
#       - Reading the file
#       - Validating the file
#       - Load file into pandas dataframe
#       - Make some calculations
#       - Iterating through the pandas rows and for each row:
#             - Load docx file template and replace the placeholders with the values from the row
#             - Save the docx file as PDF
# '''


# import pandas as pd
# import docx

# class FileProcessor:
#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.dataframe = None
    
#     def read_xlsx(self):
#         """Reads the .xlsx file and loads it into a pandas dataframe"""
#         self.dataframe = pd.read_excel(self.file_path)
    
#     def validate(self):
#         """Validates the file"""
#         # Add validation logic here
#         pass
    
#     def calculations(self):
#         """Make some calculations on the dataframe"""
#         # Add calculation logic here
#         pass
    
#     def process_rows(self, template_path):
#         """Iterates through the rows of the dataframe and generates a PDF for each row"""
#         for index, row in self.dataframe.iterrows():
#             doc = docx.Document(template_path)
#             for paragraph in doc.paragraphs:
#                 for key, value in row.items():
#                     paragraph.text = paragraph.text.replace(f"{{{key}}}", str(value))
#             doc.save(f"{row['Name']}.pdf")
