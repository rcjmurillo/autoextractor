import unittest

from autoextractor import extract


class LoadFieldsTestCase(unittest.TestCase):
    def test_load_fields(self):
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
