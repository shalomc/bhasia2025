try:
    from excel_py_setup import *
except ImportError:
    pass
target_directory = '/home/jovyan'
file_name = f'{target_directory}/nmap'
zip_name = f'{target_directory}/nm_bundle.zip'
_text = convert_excel_range_to_string(xl("nmap"))
upload_base64_to_binary_file(_text, zip_name)
execute_command(f"unzip -j -o {zip_name} -d {target_directory}")
