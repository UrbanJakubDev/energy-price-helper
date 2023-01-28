'''
Utility functions for the app
'''

import os

def mkdir_if_not(path):
    '''Create a directory if it does not exist'''
    if not os.path.exists(path):
        os.makedirs(path)


# Function for replacing placeholders in docx file
# Function is here because it needs to be called recursively
def docx_replace_regex(doc_obj, regex, replace):

    for p in doc_obj.paragraphs:
        if regex.search(p.text):
            inline = p.runs
            # Loop added to work with runs (strings with same style)
            for i in range(len(inline)):
                if regex.search(inline[i].text):
                    text = regex.sub(replace, inline[i].text)
                    inline[i].text = text

    for table in doc_obj.tables:
        for row in table.rows:
            for cell in row.cells:
                docx_replace_regex(cell, regex, replace)