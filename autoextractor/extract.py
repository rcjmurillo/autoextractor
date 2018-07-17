import re
import csv

FIELD_SEP = ';'

# Fields that appear in the file
F_NUMBER = 0  # Present in the file but not usable as feature
F_ASPIRATION = 1
F_BODY_STYLE = 2
F_BORE = 3
F_CITY_MPG = 4
F_COMPRESSION_RATIO = 5
F_CURB_WEIGHT = 6
F_DRIVE_WHEELS = 7
F_ENGINE_LOCATION = 8
F_ENGINE_SIZE = 9
F_ENGINE_TYPE = 10
F_FUEL_SYSTEM = 11
F_FUEL_TYPE = 12
F_HEIGHT = 13
F_HIGHWAY_MPG = 14
F_HORSEPOWER = 15
F_LENGTH = 16
F_MAKE = 17
F_NORMALIZED_LOSSES = 18
F_NUM_OF_CYLINDERS = 19
F_NUM_OF_DOORS = 20
F_PEAK_RPM = 21
F_PRICE = 22
F_STROKE = 23
F_WEIGHT = 24
F_WHEEL_BASE = 25
F_WIDTH = 26

FIELDS_TO_EXTRACT = (
    F_ENGINE_LOCATION,
    F_NUM_OF_CYLINDERS,
    F_ENGINE_SIZE,
    F_WEIGHT,
    F_HORSEPOWER,
    F_ASPIRATION,
    F_PRICE,
    F_MAKE,
)
FIELDS_ORDER = {f: n for n, f in enumerate(FIELDS_TO_EXTRACT)}

assert F_NUMBER not in FIELDS_TO_EXTRACT, \
    'The number of the row should not be used as feature for model training'

_offsets_map = {}
_loaded_filepath = None


def load(filepath):
    """
    Create an in-memory map of row -> [(offset_in_file, value_length), ...] for the file at
    filepath mapping each row to the offsets where the data for each field start and ends.
    """
    global _offsets_map
    global _loaded_filepath

    _offsets_map = {}  # Reset the map
    _loaded_filepath = filepath

    with open(filepath) as f:
        reader = csv.reader(f, delimiter=FIELD_SEP)
        offset = 0  # Keep track of the current offset in the file
        for n, row in enumerate(reader):
            skip_row = False
            row_len = len(row)
            offset_pairs = [None] * len(FIELDS_TO_EXTRACT)
            for i, val in enumerate(row):
                val_len = len(val)
                if i in FIELDS_TO_EXTRACT:
                    # If one of the fields that we want to extract doesn't contain data
                    # skip the row
                    if val.strip() == '-':
                        skip_row = True

                    offset_pairs[FIELDS_ORDER[i]] = (offset, val_len)
                offset += val_len
                if i < row_len - 1:  # Don't count the field separator for the last field
                    offset += 1  # + 1 to count the field separator ";"

            offset += 1  # + 1 to count the line separator
            if not skip_row:
                _offsets_map[n] = offset_pairs


def get_field_offsets():
    return _loaded_filepath, _offsets_map.items()
