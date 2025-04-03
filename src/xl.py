# the purpose of this code is to provide
# a simulated local environment for testing the xl module locally

import pandas

def read_file_to_dataframe(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        # Create a DataFrame from the lines
        df = pandas.DataFrame({'Lines': [line.strip() for line in lines]})
    except:
        df = pandas.DataFrame({'Lines': [f'error reading file {file_path}']})
    return df


def xl(*parms):
    default_response_mapping = {
        'COMMAND_TO_RUN': None,
        'CHMOD_EXECUTE': False,
        'CONVERT_TO_BASE64': False,
        'UPLOADED_FILE_NAME': "myshell-2.sh",
        'Base64_data': read_file_to_dataframe("myshell.sh"),
        'persistence_location': "persistence.txt",
        'jupyter_cookie_secret': "jupyter_cookie_secret_example",
    }
    return default_response_mapping.get(parms[0], None)
