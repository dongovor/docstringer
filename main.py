import config
import utils


def main():
    try:
        check_results = {}
        # Prompt user for input file/folder path
        input_path = input("Please enter the path to the file/folder you'd like to check ").strip('"').strip("'").strip()

        is_file = utils.is_file(input_path)
        if is_file:
            check_results[input_path] = utils.check_docstrings(input_path)
        else:
            check_results = utils.iterate_through_folder(input_path)

        # Prepare save file variables 
        project_name = utils.get_project_name(input_path)
        path_to_save = utils.path_to_save(project_name)
        
        # Delete previously created json file if config.REMOVE_PREVIOUS_FILE == True
        if config.REMOVE_PREVIOUS_FILE:
            utils.remove_previous_json(path_to_save)

        # Write results to JSON file    
        utils.write_to_json(path_to_save, check_results)

        # uncomment the following line to display the contents of the created file
        utils.test_resuls(path_to_save)

    except Exception as main_error:
        print(main_error)

if __name__ == '__main__':
    try:
        main()
    except Exception as main_error:
        print(main_error)
        