from os import path,system, makedirs
from time import sleep
import subprocess
import json


def generate_package_strings(data, package_strings_list):
    """
    Generates a list of packages with versions maintaining the dependency order
    :param data: JSON containing the dependencies from pipdeptree utility
    :param package_strings_list: List containing the list of packages (blank in starting) used for storing th final list in recursion
    :return: None
    """
    try:
        for package in data:
            package_string = f"{package['key']}=={package['installed_version']}"
            if package_string not in package_strings_list:
                package_strings_list.append(package_string)
            if 'dependencies' in package:
                generate_package_strings(package['dependencies'], package_strings_list)
    except Exception as e:
        print(f'Exception encountered in generating package strings: {e}')


def get_requirements_file(file_path):
    """
    It generates a requirements.txt file with all the dependencies present in the required order.
    :param file_path: path to store temporary files and final output files
    :return: None
    """
    try:
        package_strings_list = []
        # writing the output of the pipdeptree to disk and load it again to memory
        try:
            temp_file_path = path.join(file_path, 'reverse_pipdeptree.txt')
            if not path.exists(file_path):
                makedirs(file_path)
            system(f'pipdeptree -r --json-tree > {temp_file_path}')
            # subprocess.run(f'pipdeptree -r --json-tree > {temp_file_path}', shell=True, check=True, text=True)
            with open(temp_file_path, "r") as file:
                output = file.read()
            deptree = json.loads(output)
        except Exception as e:
            print(f'Exception encountered in writing the output of the pipdeptree to disk and load it again to memory: {e}')
            exit()

        # Generate the list of package strings with no duplicates while maintaining order of dependency
        generate_package_strings(deptree, package_strings_list)

        # Write the list of package strings to a file sequentially
        try:
            with open(path.join(file_path, 'requirements_with_dependency_order.txt'), 'w') as file:
                for package_string in package_strings_list:
                    file.write(package_string + '\n')
        except Exception as e:
            print(f'Exception encountered in writing the list of package strings to a file sequentially: {e}')

    except Exception as e:
        print(f'Exception encountered: {e}')

    print("Packages saved to 'requirements_with_dependency_order.txt' file in the file_path mentioned in arguments.")


if __name__ == "__main__":
    file_path = "E:\\dependency_maker"
    get_requirements_file(file_path)
