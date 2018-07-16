from collections import OrderedDict

# Transformer functions


def one_hot_encode_transformer(values):
    """
    Transform the categorical value vector into a binary matrix where each categorical value
    becomes a column with 0 or 1 as value.
    e.g.

    ['color', 'white', 'black', 'white', 'green']

    becomes:

    [
        ['color_white', 'color_black', 'color_green'],
        [            1,             0,             0],
        [            0,             1,             0],
        [            1,             0,             0],
        [            0,             0,             1]
    ]
    """
    # First pass: find all the categorical values and assign them a number
    n = 0
    value_list = []
    values_iter = iter(values)
    header = next(values_iter)
    value_index_map = OrderedDict()
    for val in values_iter:
        # Create a list of the values for the second pass
        value_list.append(val)
        if val not in value_index_map:
            value_index_map[val] = n
            n += 1

    # Second pass: create the binary matrix
    row_length = len(value_index_map.keys())
    # Generate the header
    yield ['{0}_{1}'.format(header, val) for val in value_index_map.keys()]
    # Generate the binary vectors
    for val in value_list:
        bin_vector = [0] * row_length
        bin_vector[value_index_map[val]] = 1
        yield bin_vector


def number_str_to_int_transformer(value):
    number_str_to_int = {
        'zero': 0,
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
    }
    return number_str_to_int[value.lower()]


def german_to_english_number_notation_transformer(value):
    return value.replace('.', '').replace(',', '.')


def make_value_is_equal_transformer(true_value):
    true_value = true_value.lower()
    return lambda value: 1 if value.lower() == true_value else 0


def make_units_transformer(op, op_val):
    return lambda value: op(float(value), float(op_val))


def make_str_encode_transformer(encoding='utf-8'):
    return lambda value: value.encode(encoding)
