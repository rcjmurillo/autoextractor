import unittest

from autoextractor import extract


class TestLoadFields(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Store the default fields to use them later
        cls.default_fields = extract.FIELDS_TO_EXTRACT

    def tearDown(self):
        # Reset the default fields to extract after each test
        extract.FIELDS_TO_EXTRACT = self.default_fields
        extract.FIELDS_ORDER = {f: n for n, f in enumerate(extract.FIELDS_TO_EXTRACT)}

    def test_load_default_fields(self):
        extract.load('tests/test_data.txt')

        expected_offsets_map = {
            0: [(80, 15), (202, 16), (96, 11), (254, 6), (161, 10), (1, 10), (241, 5), (179, 4)],
            1: [(312, 5), (366, 4), (318, 3), (393, 1), (344, 6), (280, 3), (380, 7), (358, 3)],
            2: [(444, 5), (499, 4), (450, 2), (523, 1), (475, 6), (410, 5), (511, 6), (489, 5)],
            3: [(571, 5), (626, 4), (577, 3), (654, 1), (603, 6), (539, 3), (641, 7), (617, 4)],
        }

        self.assertEqual(expected_offsets_map, extract._offsets_map)

    def test_load_other_fields(self):
        # Replace extract.FIELDS_TO_EXTRACT with the fields we want to test
        extract.FIELDS_TO_EXTRACT = (extract.F_FUEL_TYPE, extract.F_BODY_STYLE, extract.F_MAKE)
        extract.FIELDS_ORDER = {f: n for n, f in enumerate(extract.FIELDS_TO_EXTRACT)}
        extract.load('tests/test_data.txt')

        expected_offsets_map = {
            0: [(132, 9), (12, 10), (179, 4)],
            1: [(331, 3), (284, 5), (358, 3)],
            2: [(462, 3), (416, 5), (489, 5)],
            3: [(590, 3), (543, 5), (617, 4)],
        }

        self.assertEqual(expected_offsets_map, extract._offsets_map)

    def test_load_and_skip_rows(self):
        # Replace extract.FIELDS_TO_EXTRACT with the fields we want to test
        extract.FIELDS_TO_EXTRACT = (extract.F_MAKE, extract.F_NUM_OF_DOORS)
        extract.FIELDS_ORDER = {f: n for n, f in enumerate(extract.FIELDS_TO_EXTRACT)}
        extract.load('tests/test_data.txt')

        expected_offsets_map = {
            0: [(179, 4), (219, 12)],
            1: [(358, 3), (371, 3)],
            # Row with index 2 must not be present since the field num-of-doors is "-" (NA)
            3: [(617, 4), (631, 4)],
        }

        self.assertEqual(expected_offsets_map, extract._offsets_map)

if __name__ == '__main__':
    unittest.main()
