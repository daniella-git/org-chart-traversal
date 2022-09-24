from unittest import TestCase, main
import org_hierarchy_functions


class TestOrganisationHierarchy(TestCase):

    # === FUNCTIONAL TESTS ===
    def test_path_that_contains_root_of_hierarchy(self):
        result = org_hierarchy_functions.get_employee_chain('hierarchy_tree.txt', 'Batman', 'Super Ted')
        expected = "Batman (16) -> Black Widow (6) -> Gonzo the Great (2) -> Dangermouse (1)" \
                   " <- Invisible Woman (3) <- Super Ted (15)"
        self.assertIn(expected, result)

    def test_path_without_root_of_hierarchy(self):
        result = org_hierarchy_functions.get_employee_chain('hierarchy_tree.txt', 'Batman', 'Catwoman')
        expected = "Batman (16) -> Black Widow (6) <- Catwoman (17)"
        self.assertIn(expected, result)

    def test_path_between_employee_and_their_manager(self):
        result = org_hierarchy_functions.get_employee_chain('hierarchy_tree.txt', 'Batman', 'Gonzo the great')
        expected = "Batman (16) -> Black Widow (6) -> Gonzo the Great (2)"
        self.assertIn(expected, result)

    def test_paths_for_multiple_employees_with_the_same_name(self):
        result = org_hierarchy_functions.get_employee_chain('hierarchy_tree.txt', 'Batman', 'Catwoman')
        expected_1 = "Batman (16) -> Black Widow (6) <- Catwoman (17)"
        expected_2 = "Batman (16) -> Black Widow (6) -> Gonzo the Great (2) -> Dangermouse (1) <- Catwoman (18)"
        self.assertIn(expected_1, result)
        self.assertIn(expected_2, result)

    def test_path_with_differently_formatted_names(self):
        result = org_hierarchy_functions.get_employee_chain('hierarchy_tree.txt', 'batman  ', '   gonZO   the GREAT ')
        expected = "Batman (16) -> Black Widow (6) -> Gonzo the Great (2)"
        self.assertIn(expected, result)

    def test_path_between_two_employees_of_same_name(self):
        result = org_hierarchy_functions.get_employee_chain('hierarchy_tree.txt', 'Catwoman', 'Catwoman')
        expected_1 = "Catwoman (17) -> Black Widow (6) -> Gonzo the Great (2) -> Dangermouse (1) <- Catwoman (18)"
        expected_2 = "Catwoman (18) -> Dangermouse (1) <- Gonzo the Great (2) <- Black Widow (6) <- Catwoman (17)"
        self.assertIn(result[0], [expected_1, expected_2])

    # === UNIT TESTS ===
    def test_parse_employee_data(self):
        employees, managers = org_hierarchy_functions.parse_employee_data(['| 16      | Batman  |      6|'])
        employee = employees[0]

        self.assertEqual("16", employee.id)
        self.assertEqual("Batman", employee.name)
        self.assertEqual("6", employee.manager_id)

        self.assertEqual(employee.manager_id, managers[employee.id])

    def test_ensure_employee_combination_uniqueness(self):
        employee_set = org_hierarchy_functions.ensure_employee_combination_uniqueness(["17", "18"], ["17", "18"])
        expected = {("17", "18")}
        self.assertEqual(expected, employee_set)

    def test_find_path_to_root(self):
        path_to_root = org_hierarchy_functions.find_path_to_root("16", {"1": None, "2": "1", "6": "2", "16": "6"})
        expected = ["16", "6", "2", "1"]
        self.assertEqual(expected, path_to_root)

    def test_connect_paths(self):
        connected_paths = org_hierarchy_functions.connect_paths(["6", "4", "2", "1"], ["7", "5", "3", "2", "1"])
        expected = (["6", "4"], "2", ["3", "5", "7"])
        self.assertEqual(expected, connected_paths)

    def test_connect_paths_with_no_divergence(self):
        connected_paths = org_hierarchy_functions.connect_paths(["16", "6", "2", "1"], ["6", "2", "1"])
        expected = (["16"], "6", [])
        self.assertEqual(expected, connected_paths)

    def test_connect_paths_with_no_left_path(self):
        connected_paths = org_hierarchy_functions.connect_paths(["1"], ["2", "1"])
        expected = ([], "1", ["2"])
        self.assertEqual(expected, connected_paths)


if __name__ == '__main__':
    main()
