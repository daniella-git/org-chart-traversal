import sys
from org_hierarchy_functions import get_employee_chain


def main():
    arguments = sys.argv
    if len(arguments) != 4:
        print("Incorrect number of arguments provided. Expected 3, got {}".format(len(arguments) - 1))
        sys.exit(1)
    file_path = arguments[1]
    employee_1_name = arguments[2]
    employee_2_name = arguments[3]
    formatted_paths = get_employee_chain(file_path, employee_1_name, employee_2_name)
    for path in formatted_paths:
        print(path)


if __name__ == "__main__":
    main()
