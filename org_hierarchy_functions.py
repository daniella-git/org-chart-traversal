def get_employee_chain(file_path, employee_1_name, employee_2_name):
    """
    Finds the shortest chain between two given employees and the path to a file including all employee data.
    If multiple employees with the same name exist in the data, paths between all combinations of employees with
    the given names will be returned.

    :param file_path: Path to employee data file.
    :param employee_1_name: An Employee name.
    :param employee_2_name: Another Employee name.
    :return: List of strings representing chains between the named employees.
    """

    employees, managers = get_employees_from_file(file_path)

    employee_1_ids = find_employee_ids(employee_1_name, employees)
    employee_2_ids = find_employee_ids(employee_2_name, employees)

    unique_employee_combinations = ensure_employee_combination_uniqueness(employee_1_ids, employee_2_ids)

    paths_to_format = find_paths(unique_employee_combinations, managers)
    formatted_paths = [format_path(*path, employees=employees) for path in paths_to_format]

    return formatted_paths


def find_paths(employee_pairs, managers):
    """
    Finds paths between employees. Where there are multiple employee ids for a given employee name,
    paths will be found between all combinations of employee 1 and 2.

    :param employee_pairs: set of tuples containing unique employee combinations
    :param managers: dictionary mapping employee_id to manager_id
    :return: paths between all combinations of employee 1 and 2 ids in the format
    (<left_path>, <intersection>, <right_path>)
    """
    paths = []
    for employee_1_id, employee_2_id in employee_pairs:
        employee_1_path = find_path_to_root(employee_1_id, managers)
        employee_2_path = find_path_to_root(employee_2_id, managers)
        left_path, intersection, right_path = connect_paths(employee_1_path, employee_2_path)
        paths.append((left_path, intersection, right_path))
    return paths


def get_employees_from_file(file_path):
    """
    Loads the file at the path provided and parses the contents.

    :param file_path: Path to employee data file.
    :return: (employees, managers) where employees is a List of Employees and managers is a mapping between
    employee ids and their manager's id.
    """

    with open(file_path) as file:
        file_contents = file.readlines()
    return parse_employee_data(file_contents[1:])  # skip the header row by slicing


def parse_employee_data(file_contents):
    """
    Converts lines of text into employee data.

    Expects employee data to be in the format "| <employee_id> | <employee_name> | <manager_id> |".

    :param file_contents: list of lines from the employee data file.
    :return: (employees, managers)
        employees: list of employee objects ['employee_id', 'employee_name', 'manager_id']
        managers: dictionary mapping employee_id to manager_id
    """

    employees = []
    managers = {}
    for employee_line in file_contents:
        split_line = employee_line.split("|", 4)
        employee_id, employee_name, manager_id = [data.strip() for data in split_line[1:4]]
        managers[employee_id] = manager_id if manager_id != "" else None
        employees.append(Employee(employee_id, employee_name, manager_id))

    return employees, managers


def reformat_employee_name(employee_name):
    """
    Converts an arbitrarily formatted employee name into a standardised one for comparison.

    Employee names are converted to lowercase, split into individual words, extra spaces are stripped and they are
    joined into one string. For example, "  gonzo   ThE    GREAt  " and "Gonzo the GREAT" are both reformatted into
    "gonzo the great".

    :param employee_name: The employee name to reformat.
    :return: The reformatted employee name.
    """
    employee_name = employee_name.lower().split()
    employee_words = [word.strip() for word in employee_name]
    return " ".join(employee_words)


def ensure_employee_combination_uniqueness(employee_1_ids, employee_2_ids):
    """
    Prevent repeated combinations of employee ids where employees share a name.

    :param employee_1_ids: list of employee ids
    :param employee_2_ids: list of employee ids
    :return: set of unique employee combinations, in the format: {(<employee_1_id>, <employee_2_id>)}
    """
    employee_set = set()
    for employee_1 in employee_1_ids:
        for employee_2 in employee_2_ids:
            if (employee_2, employee_1) not in employee_set and employee_1 != employee_2:
                employee_set.add((employee_1, employee_2))
    return employee_set


def find_employee_ids(employee_name, employees):
    """
    Given an employee name, return a list of corresponding employee ids.

    :param employee_name: The name of the employee to search for.
    :param employees: The list of all employees.
    :return: A list of ids of employees with the given name.
    """
    employee_ids = []
    for employee in employees:
        if reformat_employee_name(employee.name) == reformat_employee_name(employee_name):
            employee_ids.append(employee.id)
    return employee_ids


def find_path_to_root(employee_id, managers):
    """
    Returns the chain of manager employee ids for a given employee.

    :param employee_id: The employee id to start from.
    :param managers: The mapping between employees and their managers.
    :return: A list of ids from the given employee_id to the root of the hierarchy.
    """
    path_list = []
    while employee_id is not None:
        path_list.append(employee_id)
        employee_id = managers[employee_id]
    return path_list


def connect_paths(path_1, path_2):
    """
    Return the path to and from the lowest depth manager that two employees share.

    Searching is done from the root of the hierarchy down for efficiency, since comparisons will only occur between
    employees at the same level.

    Starting from the top of the hierarchy, descend until the paths diverge:
    e.g. paths [6, 4, 2, 1], [7, 5, 3, 2, 1] would return [6, 4], 2, [3, 5, 7]

    :param path_1: The path from the first employee to the root of the hierarchy.
    :param path_2: The path from the second employee to the root of the hierarchy.
    :return: (left_path, intersection, right_path)
    """
    reversed_path_1 = path_1[::-1]
    reversed_path_2 = path_2[::-1]
    max_search_depth = min(len(path_1), len(path_2))  # we can only search as deep as the shallowest path

    depth = 0
    while depth <= max_search_depth:
        if depth == max_search_depth or reversed_path_1[depth] != reversed_path_2[depth]:
            left_path = path_1[:-depth]
            intersection = reversed_path_1[depth - 1]
            right_path = reversed_path_2[depth:]
            return left_path, intersection, right_path
        depth += 1


def get_employee_names(employees):
    """
    Create a mapping between employee ids and their original names.

    :param employees: List of employees.
    :return: mapping between employee ids and their original names.
    """
    employee_names = {}
    for employee in employees:
        employee_names[employee.id] = employee.name
    return employee_names


def format_path(path_1, target, path_2, employees):
    """
    Converts a chain of employee ids to a formatted string representation.

    Given [16, 6, 2], 1, [3, 15], List<Employee> (with superhero names!), the function returns:
    Batman (16) -> Black Widow (6) -> Gonzo the Great (2) -> Dangermouse (1) <- Invisible Woman (3) <- Super Ted (15)

    :param path_1: Path from employee 1 to the lowest depth common manager (exclusive).
    :param target: Lowest depth common manager id.
    :param path_2: Path from employee 2 to the lowest depth common manager (exclusive).
    :param employees: List of all employees.
    :return: A string representation of the chain between two employees.
    """
    employee_id_name = get_employee_names(employees)
    formatted_path = ""

    for employee_id in path_1:
        employee_name = employee_id_name[employee_id]
        reformat_employee = "{} ({}) -> ".format(employee_name, employee_id)
        formatted_path = formatted_path + reformat_employee

    formatted_path = formatted_path + employee_id_name[target] + " ({})".format(target)

    for employee_id in path_2:
        employee_name = employee_id_name[employee_id]
        reformat_employee = " <- {} ({})".format(employee_name, employee_id)
        formatted_path = formatted_path + reformat_employee

    return formatted_path


class Employee:
    """
    Class to hold information about a given employee.
    """

    def __init__(self, e_id, name, manager_id):
        self.id = e_id
        self.name = name
        self.manager_id = manager_id







