import re
import operator

from autoextractor import extract
from .extract import (
    F_ASPIRATION,
    F_ENGINE_LOCATION,
    F_ENGINE_SIZE,
    F_HORSEPOWER,
    F_MAKE,
    F_NUM_OF_CYLINDERS,
    F_PRICE,
    F_WEIGHT,
)
from .transformers import (
    one_hot_encode_transformer,
    number_str_to_int_transformer,
    german_to_english_number_notation_transformer,
    make_value_is_equal_transformer,
    make_units_transformer,
    make_str_encode_transformer
)


# Tranformation definition for each field
field_transforms = {
    F_ENGINE_LOCATION: [one_hot_encode_transformer],
    F_NUM_OF_CYLINDERS: [number_str_to_int_transformer],
    F_ENGINE_SIZE: [german_to_english_number_notation_transformer, int],
    F_WEIGHT: [int],
    F_HORSEPOWER: [german_to_english_number_notation_transformer, float],
    F_ASPIRATION: [make_value_is_equal_transformer('turbo')],
    F_PRICE: [make_units_transformer(operator.truediv, 100)],
    F_MAKE: [make_str_encode_transformer()]
}


def _read_values(filepath):
    def read_from_file(f, offset, length):
        f.seek(offset)
        return f.read(length)

    with open(filepath) as f:
        for n, offset_pairs in extract.get_field_offsets():
            yield n, (read_from_file(f, offset, length) for offset, length in offset_pairs)


def transform(filepath):
    for n, values in _read_values(filepath):
        print(n, list(values))
