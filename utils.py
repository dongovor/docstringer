import os
import ast
import json
import pathlib
import getpass

def check_os_type():
    """
    Returns the name of the operating system.

    Returns:
        os.type (bool): The name of the operating system (e.g. 'posix' or 'nt'
    """
    return os.name

def is_file(input_path):
    """
    Checks if the given filepath is a file.

    Parameters:
    input_path (str): The path of the file to check.

    Returns:
    bool: True if the filepath is a file, False otherwise.
    """
    return os.path.isfile(input_path)

def check_docstrings(file_path):
    """
    Checks if a Python file has docstrings for each class and method,
    and prints the names of those that do not have docstrings.

    Parameters:
    file_path (str): The path of the Python file to check.
    """
    no_docstrings = []

    with open(file_path, 'r') as file:
        try:
            contents = ast.parse(file.read())
        except SyntaxError:
            print(f"Error: Could not parse file {file_path}.")
            return
    
    for node in ast.walk(contents):        
        args_list = get_method_args(node)
        args_string = ",".join(args_list) 
        
        if args_string != "":
            args_string = f';{args_string}'

        if isinstance(node, ast.ClassDef):
            if not node.body or not isinstance(node.body[0], ast.Expr) or not isinstance(node.body[0].value, ast.Str):
                no_docstrings.append(f'{node.name}{";" if args_string != "" else ""}')

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.body or not isinstance(node.body[0], ast.Expr) or not isinstance(node.body[0].value, ast.Str):
                no_docstrings.append(f'{node.name}{args_string}')

    return no_docstrings

def get_method_args(node):
    """
    Gets the arguments of a method.

    Parameters:
    node (ast): The node to get the arguments from.

    Returns:
    str: The arguments of the method.
    """
    args_list = []
    try:
        for arg in node.args.args:
            args_list.append(arg.arg)
    except AttributeError:
        pass

    return args_list

def iterate_through_folder(folderpath):
    """
    Iterates through the files of a given folder and calls check_docstrings on each file.

    Parameters:
    folderpath (str): The path of the folder to iterate through.
    """
    checked_files = {}

    try:
        for filename in os.listdir(folderpath):
            filepath = os.path.join(folderpath, filename)
            
            if not is_py_file(filepath):
                continue

            print(f'Checking: {filepath}')
            if os.path.isfile(filepath):
                result = check_docstrings(filepath)
                checked_files[filepath.replace(getpass.getuser(), "<username>")] = result
    except FileNotFoundError:
        print(f"Error: Folder not found at {folderpath}. Please try again.")

    return checked_files

def write_to_json(file_path: str, checked_files: dict):
    """
    Writes the results of the docstring checks to a JSON file.

    Parameters:
    checked_files (dict): A dictionary containing the results of the docstring checks.
    """
    try:
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as file:
                json.dump(checked_files, file)
        else:
            with open(file_path, 'r') as file:
                json_data = json.load(file)
            
            json_data.update(checked_files)

            with open(file_path, 'w') as file:
                json.dump(json_data, file, indent=4)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}. Unable to append dictionary to JSON file.")
        return False

def test_resuls(path_to_json: str):
    """
    Print results from provided json.

    Parameters:
    path_to_json (str): Path to results json file.
    """
    # read results from JSON file
    with open(path_to_json, 'r') as file:
        results = json.load(file)
    
    for result in results:
        if len(results[result]) != 0:
            print(f'File: {result}')
            for res in results[result]:
                try:
                    print(f'\t- Method: {str(res).split(";")[0]}')
                    if len(str(res).split(";")) == 1:
                        continue
                    
                    if len(str(res).split(";")[1].split(",")) != 0:
                        for arg in str(res).split(";")[1].split(","):
                            print('\t\tArguments:')
                            print(f'\t\t\t- {arg}')
                except Exception as ouch:
                    print(ouch)

def remove_newlines(string):
    return string.replace('\r', '').replace('\n', '')

def get_project_name(path_to_project: str):
    """
    Returns basename.

    Parameters:
    path_to_project (str): Path to project.

    Returns:
    basename (str): Project basename.
    """
    basename = os.path.basename(path_to_project)
    return basename

def path_to_save(basename: str):
    """
    Returns full path to save.

    Paremeters:
    basename (str): Project name.

    Returns:

    path_to_save (str): Path to save json. 
    """
    path_to_save = os.path.join(os.path.dirname(__file__), f'{basename}.json')
    return path_to_save

# in the following two methods, docstrings were not added on purpose
def remove_previous_json(path_to_file: str):
    if os.path.isfile(path_to_file):
        os.remove(path_to_file)

def is_py_file(path_to_file: str):
    is_py_file = False
    if pathlib.Path(path_to_file).suffix == '.py':
        is_py_file = True
    return is_py_file

# bellow two dummy methods for testing
def dummy_function_without_doctring():
    pass

def another_function_without_doctring(first_arg: str, second_arg: int, third_arg = []):
    pass
