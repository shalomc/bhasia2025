import base64
import os
import subprocess
"""
See README.md for more information on how to use this script 
and how to set up excel
"""

# We have a local xl module that we can use to simulate the xl module in Azure for local development
try:
    from xl import xl
except ImportError:
    pass

# Global variables
# Unfortunately we can't use the built-in xl module to get indirect references, so we have to hardcode the ranges

# All of the BASE64 data as a pandas dataframe
EXCEL_BASE64_PAYLOAD_DATA = xl("Base64_data")

# Boolean flag to determine if the data should be converted from BASE64 before writing to a file.
# Set to False if the data is not in BASE64 format, like shell scripts or text files.
EXCEL_BASE64_CONVERT_BOOLEAN_FLAG = xl("CONVERT_FROM_BASE64")

# The name of the file to upload, the script will create this file in the HOME directory
EXCEL_NAME_OF_FILE_TO_UPLOAD = xl("UPLOADED_FILE_NAME")

# Boolean flag to determine if the file should be made executable
EXCEL_CHMOD_EXECUTE_BOOLEAN_FLAG = xl("CHMOD_EXECUTE")

# The command to run for verification after the file is uploaded. If empty or None, no command will be run.
EXCEL_COMMAND_TO_RUN_AFTER_UPLOAD = xl("Execute_Command_on_Upload")

IS_AZURE = 'OfficePy__ComputeResourceId' in os.environ


def set_environment():
    HOME = os.environ.get('HOME', '/home/jovyan')
    LD_LIBRARY_PATH = os.environ.get('LD_LIBRARY_PATH')
    LD_LIBRARY_PATH = [] if LD_LIBRARY_PATH is None else LD_LIBRARY_PATH.split(':')
    if not HOME in LD_LIBRARY_PATH: LD_LIBRARY_PATH.insert(0,HOME)
    os.environ['LD_LIBRARY_PATH'] = ':'.join(LD_LIBRARY_PATH)
    EXECUTION_PATH = os.environ.get('PATH')
    EXECUTION_PATH = [] if EXECUTION_PATH is None else EXECUTION_PATH.split(':')
    if not HOME in EXECUTION_PATH: EXECUTION_PATH.insert(0,HOME)
    os.environ['PATH'] = ':'.join(EXECUTION_PATH)



def convert_base64_to_executable(base64_string, output_file_path):
    # Decode the Base64 string into binary data
    binary_data = base64.b64decode(base64_string)

    # Write the binary data to a file
    with open(output_file_path, "wb") as binary_file:
        binary_file.write(binary_data)
    print(f"Binary file '{output_file_path}' created successfully!")

def upload_direct(upload_data, output_file_path):
    with open(output_file_path, "w") as text_file:
        text_file.write(upload_data)
    print(f"Text file '{output_file_path}' created successfully!")

base64_payload = xl("Base64_data")
payload_dir = dir(base64_payload)
column_name = base64_payload.columns[0]
base64_string = base64_payload[column_name].str.cat(sep='\n')
executable_file = xl("UPLOADED_FILE_NAME")  # Name of the binary file to create
if IS_AZURE:
    output_file_path = f'{os.environ["HOME"]}/{executable_file}'
else:
    output_file_path = executable_file  # Name of the binary file to create

if xl("CONVERT_FROM_BASE64"):
    # Convert the Base64 string back to an executable binary file
    convert_base64_to_executable(base64_string, output_file_path)
else:
    # Upload the data directly
    upload_direct(base64_string, output_file_path)
# Now, make the file executable using the os module

if xl("CHMOD_EXECUTE"):
    os.chmod(output_file_path, 0o755)  # Makes the file executable

print(f"File '{output_file_path}' is now executable!")

# Define the command you want to run
try:
    command_to_execute = xl("Execute_Command_on_Upload")
except:
    command_to_execute = './nc -h'

if command_to_execute is not None:
# Execute the command and capture the output
    set_environment()
    result = subprocess.run(command_to_execute, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # Split the output into a list of lines
    output_lines = result.stdout.splitlines()
    error_lines = result.stderr.splitlines()
    print(output_lines + error_lines)
else:
    output_lines = [f"Uploaded file {output_file_path}", "Nothing to execute"]
    error_lines = []

output_lines + error_lines
