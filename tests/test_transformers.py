# coding: utf-8
import operator
import unittest
from collections import defaultdict, OrderedDict

from autoextractor import transformers
from autoextractor.transformers import (
    build_one_hot_encode_map,
    make_one_hot_encode_transformer,
    number_str_to_int_transformer,
    german_to_english_number_notation_transformer,
    make_value_is_equal_transformer,
    make_units_transformer,
    make_str_encode_transformer
)


class TransformersTestCase(unittest.TestCase):
    def setUp(self):
        transformers._one_hot_encode_map = defaultdict(OrderedDict)

    def test_one_hot_encode_transformer(self):
        build_one_hot_encode_map(1, ['color', 'white', 'black', 'green', 'black'])
        build_one_hot_encode_map(2, ['aspiration', 'sedan', 'turbo', 'hatchback'])
        cases = {
            1: [
                ('white', [1, 0, 0]),
                ('black', [0, 1, 0]),
                ('green', [0, 0, 1]),
            ],
            2: [
                ('sedan', [1, 0, 0]),
                ('hatchback', [0, 0, 1]),
                ('turbo', [0, 1, 0]),
            ],
        }

        for field, values in cases.items():
            transform = make_one_hot_encode_transformer(field)
            for value, expected in values:
                self.assertEqual(expected, list(transform(value)))

    def test_number_str_to_int_transformer(self):
        cases = [
            # All one digit numbers
            ('zero', 0),
            ('one', 1),
            ('two', 2),
            ('three', 3),
            ('four', 4),
            ('five', 5),
            ('six', 6),
            ('seven', 7),
            ('eight', 8),
            ('nine', 9),
            # Other cases
            ('One', 1),
            ('twO', 2),
            ('FIVE', 5),
        ]

        for num_str, expected in cases:
            self.assertEqual(expected, number_str_to_int_transformer(num_str))

    def test_german_to_english_number_notation_transformer(self):
        cases = [
            ('2.000.000,50', '2000000.50'),
            ('1,2', '1.2'),
            ('2,105', '2.105'),
            ('100.000', '100000'),
            ('4.000', '4000'),
            ('1.000', '1000'),
        ]

        for german_num_str, expected in cases:
            self.assertEqual(
                expected, german_to_english_number_notation_transformer(german_num_str))

    def test_value_is_equal_transformer(self):
        cases = [
            ('turbo', [('turbo', 1), ('sedan', 0), ('hatchback', 0)]),
            ('sedan', [('turbo', 0), ('hatchback', 0)]),
        ]

        for val_to_compare, comparisons in cases:
            transformer = make_value_is_equal_transformer(val_to_compare)
            for field_val, expected in comparisons:
                self.assertEqual(expected, transformer(field_val))

    def test_units_transformer(self):
        cases = [
            (operator.truediv, 100, [(10025, 100.25), (125, 1.25), (501, 5.01)]),
            (operator.mul, 2, [(10, 20), (5, 10), (1, 2), (7, 14)]),
        ]

        for op, op_val, values in cases:
            transformer = make_units_transformer(op, op_val)
            for val, expected in values:
                self.assertEqual(expected, transformer(val))

    def test_str_encode_transformer(self):
        cases = [
            ('utf-8', [('áeíoú', b'\xc3\xa1e\xc3\xado\xc3\xba'), ('abcñ123', b'abc\xc3\xb1123')]),
            ('latin-1', [('áeíoú', b'\xe1e\xedo\xfa'), ('abcñ123', b'abc\xf1123')]),
        ]
        for encoding, values in cases:
            transformer = make_str_encode_transformer(encoding)
            for unicode_str, expected in values:
                self.assertEqual(expected, transformer(unicode_str))
