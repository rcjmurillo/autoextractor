import operator
import unittest

from autoextractor import extract, transformer, transformers
from autoextractor.extract import F_ASPIRATION, F_PRICE, F_MAKE


class TransformTestCase(unittest.TestCase):
    def test_transformations(self):
        extract.FIELDS_TO_EXTRACT = (
            F_ASPIRATION,
            F_PRICE,
            F_MAKE,
        )
        extract.FIELDS_ORDER = {f: n for n, f in enumerate(extract.FIELDS_TO_EXTRACT)}
        extract.load('tests/test_data.txt')

        transformer.FIELDS_ORDER = extract.FIELDS_ORDER
        transformer.INV_FIELDS_ORDER = {n: f for f, n in extract.FIELDS_ORDER.items()}
        transformer.field_transforms = {
            F_ASPIRATION: [transformers.make_one_hot_encode_transformer(F_ASPIRATION)],
            F_PRICE: [transformers.make_units_transformer(operator.truediv, 100), float],
            F_MAKE: [transformers.make_str_encode_transformer()]
        }

        result = transformer.transform('tests/test_data.txt')

        expected = [
            ['aspiration_std', 'aspiration_turbo', 'price', 'make'],
            [1, 0, 16430.00, b'bmw'],
            [0, 1, 8558.00, b'dodge'],
            [1, 0, 17450.00, b'audi'],
        ]

        self.assertEqual(expected, [list(r) for r in result])
