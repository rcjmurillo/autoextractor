from collections import defaultdict, OrderedDict

_one_hot_encode_map = defaultdict(OrderedDict)
ONE_HOT_ENCODE_FUNC_NAME = 'one_hot_encode_transformer'

# Transformer functions


def build_one_hot_encode_map(field, values):
    """
    Populate the _one_hot_encode_map with all the different values found the values list
    and assign each value a number.
    """
    # Find all the categorical values and assign them a number
    n = 0
    values_iter = iter(values)
    header = next(values_iter)
    for val in values_iter:
        if val not in _one_hot_encode_map[field]:
            _one_hot_encode_map[field][val] = n
            n += 1

    return ('{0}_{1}'.format(header, k) for k in _one_hot_encode_map[field].keys())


def reset_one_hot_encode_map():
    global _one_hot_encode_map
    _one_hot_encode_map = defaultdict(OrderedDict)


def make_one_hot_encode_transformer(field):
    def transformer(value):
        """
        Transform the categorical value into a binary vector that will contain a single true value
        at the index corresponding to the categorical value according to _one_hot_encode_map.
        e.g.
        Given {'red': 0, 'blue': 1, 'green' 2} as _one_hot_encode_map the value
        'blue' yields [0, 1, 0]
        """
        # Create the binary vector
        row_length = len(_one_hot_encode_map[field].keys())
        # Generate the binary vectors
        bin_vector = [0] * row_length
        bin_vector[_one_hot_encode_map[field][value]] = 1
        return bin_vector
    transformer.__name__ = ONE_HOT_ENCODE_FUNC_NAME
    return transformer


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
    """
    Convert numbers from german to english notation eg. 1.000,45 to 1000.45
    """
    return value.replace('.', '').replace(',', '.')


def make_value_is_equal_transformer(true_value):
    true_value = true_value.lower()
    return lambda value: 1 if value.lower() == true_value else 0


def make_units_transformer(op, op_val):
    """
    Creates a transform function the will apply the provided operator and operator value
    to each value provided, useful for unit conversions.
    """
    return lambda value: op(float(value), float(op_val))


def make_str_encode_transformer(encoding='utf-8'):
    return lambda value: value.encode(encoding)
