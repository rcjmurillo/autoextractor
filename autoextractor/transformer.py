import re
import operator
import types

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
    FIELDS_ORDER
)
from .transformers import (
    ONE_HOT_ENCODE_FUNC_NAME,
    build_one_hot_encode_map,
    reset_one_hot_encode_map,
    make_one_hot_encode_transformer,
    number_str_to_int_transformer,
    german_to_english_number_notation_transformer,
    make_value_is_equal_transformer,
    make_units_transformer,
    make_str_encode_transformer
)

INV_FIELDS_ORDER = {n: f for f, n in FIELDS_ORDER.items()}

# Tranformation definition for each field, a list of functions per field.
# Each function must accept and return a value.
field_transforms = {
    F_ENGINE_LOCATION: [make_one_hot_encode_transformer(F_ENGINE_LOCATION)],
    F_NUM_OF_CYLINDERS: [number_str_to_int_transformer],
    F_ENGINE_SIZE: [german_to_english_number_notation_transformer, int],
    F_WEIGHT: [int],
    F_HORSEPOWER: [german_to_english_number_notation_transformer, float],
    F_ASPIRATION: [make_value_is_equal_transformer('turbo')],
    F_PRICE: [make_units_transformer(operator.truediv, 100)],
    F_MAKE: [make_str_encode_transformer()]
}

# Make sure all fields that are listed in extract are listed here for transformation
assert set(field_transforms.keys()) == set(extract.FIELDS_TO_EXTRACT), \
    "Fields listed for extraction and their transformations does not match."

_one_hot_encoded_headers = {}


def _build_one_hot_encoded_maps(fp, field_offsets):
    """
    Search for one-hot encoded fields in the transformation definitionand build a map
    (categorical_value -> index) from the values in the dataset.
    These maps are used later to build the binary vectors.
    """
    global _one_hot_encoded_headers
    _one_hot_encoded_headers = {}

    reset_one_hot_encode_map()
    # Build maps for one-hot encoded fields
    for field, transformers in field_transforms.items():
        for t in transformers:
            if t.__name__ == ONE_HOT_ENCODE_FUNC_NAME:
                column_values = _read_column(fp, FIELDS_ORDER[field], field_offsets)
                new_columns = build_one_hot_encode_map(field, column_values)
                _one_hot_encoded_headers[field] = new_columns


def _flatten_value(value):
    if isinstance(value, (int, float, str, bytes)):
        yield value
    elif isinstance(value, (list, tuple, types.GeneratorType)):
        for val in value:
            yield val


def _transform_value(value, transformers):
    """
    Transform the provided value using the list of transformers,
    e.g if we have value 'a' and functions f, g, h, the result will be:
        result = h(g(f('a')))
    """
    transformed_value = value.strip()
    for t in transformers:
        transformed_value = t(transformed_value)
    return transformed_value


def _read_value_from_file(fp, offset, length):
    fp.seek(offset)
    return fp.read(length)


def _read_column(fp, col_index, field_offsets):
    """
    Returns a generator that produces a vector of the specified column index from the dataset.
    """
    for n, offsets in field_offsets:
        offset, length = offsets[col_index]
        yield _read_value_from_file(fp, offset, length)


def _flatten_header(field, value):
    """
    Flatten one hot encoded headers columns by the categorical values found in the dataset
    if applicable, otherwise just return the provided value.
    """
    if field in _one_hot_encoded_headers:
        for c in _one_hot_encoded_headers[field]:
            yield c
    else:
        yield value


def _gen_headers(fp, offsets):
    """
    Generate the headers by reading the values from the file, any one-hot encoded fields
    will be replaced by their categorical values.
    """
    return (c for i, (offset, length) in enumerate(offsets)
            for c in _flatten_header(INV_FIELDS_ORDER[i],
                                     _read_value_from_file(fp, offset, length)))


def _gen_row(fp, offset_pairs):
    """
    Generate each row for the final matrix, read the values from the file using the offsets
    and apply the transformations for each field.
    """
    for i, (offset, length) in enumerate(offset_pairs):
        value = _read_value_from_file(fp, offset, length)
        transformed_value = _transform_value(value, field_transforms[INV_FIELDS_ORDER[i]])
        for val in _flatten_value(transformed_value):
            yield val


def transform(filepath):
    # Get the offsets map created with extract.load
    loaded_filepath, field_offsets = extract.get_field_offsets()

    assert filepath == loaded_filepath, \
        'The loaded file and the file to transform must be the same.'

    with open(filepath) as fp:
        # Build categorical values map for each one-hot encoded field
        _build_one_hot_encoded_maps(fp, field_offsets)

        # Generate headers row
        field_offsets_iter = iter(field_offsets)
        _, header_offsets = next(field_offsets_iter)
        yield _gen_headers(fp, header_offsets)

        # Generate rows
        for _, offset_pairs in field_offsets_iter:
            yield _gen_row(fp, offset_pairs)
