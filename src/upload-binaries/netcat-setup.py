try:
    from excel_py_setup import *
except ImportError:
    pass
nc = "/home/jovyan/nc"
libbsd = "/home/jovyan/libbsd.so.0"
libmd = "/home/jovyan/libmd.so.0"
nc_text = convert_excel_range_to_string(xl("netcat"))
libbsd_text = convert_excel_range_to_string(xl("libbsd.so.0"))
libmd_text = convert_excel_range_to_string(xl("libmd.so.0"))
upload_base64_to_binary_file(nc_text, nc)
upload_base64_to_binary_file(libbsd_text, libbsd)
upload_base64_to_binary_file(libmd_text, libmd)
make_executable(nc)
