from pandas import DataFrame

from src.machine_learning.label.common import add_label_column
from src.machine_learning.encoding.constants import TaskGenerationType, get_prefix_length, get_max_prefix_length, PrefixLengthStrategy

ATTRIBUTE_CLASSIFIER = None
PREFIX_ = 'prefix_'


def simple_features(log, prefix_length, padding, prefix_length_strategy: str, labeling_type, generation_type, feature_list: list = None, target_event: str = None) -> DataFrame:
    max_prefix_length = get_max_prefix_length(log, prefix_length, prefix_length_strategy, target_event)
    columns = _compute_columns(max_prefix_length)
    columns_number = len(columns)
    encoded_data = []
    for trace in log:
        trace_prefix_length = get_prefix_length(trace, prefix_length, prefix_length_strategy, target_event)
        if len(trace) <= prefix_length - 1 and not padding:
            # trace too short and no zero padding
            continue
        if generation_type == TaskGenerationType.ALL_IN_ONE.value:
            for event_index in range(1, min(trace_prefix_length + 1, len(trace) + 1)):
                encoded_data.append(_trace_to_row(trace, event_index, columns_number, prefix_length_strategy, padding, labeling_type))
        else:
            encoded_data.append(_trace_to_row(trace, trace_prefix_length, columns_number, prefix_length_strategy, padding, labeling_type))
    return DataFrame(columns=columns, data=encoded_data)


def _trace_to_row(trace, prefix_length: int, columns_number: int, prefix_length_strategy: str, padding: bool = True, labeling_type: str = None) -> list:
    """Row in data frame"""
    trace_row = [trace.attributes['concept:name']]
    trace_row += _trace_prefixes(trace, prefix_length)
    if padding or prefix_length_strategy == PrefixLengthStrategy.PERCENTAGE.value:
        trace_row += [0 for _ in range(len(trace_row), columns_number - 1)]
    trace_row += [add_label_column(trace, labeling_type, prefix_length)]
    return trace_row


def _trace_prefixes(trace, prefix_length: int) -> list:
    """List of indexes of the position they are in event_names

    """

    prefixes = []
    counter = 0
    for idx, event in enumerate(trace):
        for attribute_key, attribute_value in event.items():
            if counter == prefix_length:
                break
            if (attribute_key == 'concept:name'):
                event_attribute = attribute_value
                counter = counter + 1
                prefixes.append(event_attribute)
    return prefixes
"""
    prefixes = []
    for idx, event in enumerate(trace):
        if idx == prefix_length:
            break
        event_name = event["concept:name"]
        prefixes.append(event_name)
        print(prefixes)
    return prefixes
    """

def contains_numbers_iterative(string):
    for char in string:
        if char.isdigit():
            return True
    return False


def _compute_columns(prefix_length: int) -> list:
    """trace_id, prefixes, any other columns, label

    """
    return ["trace_id"] + [PREFIX_ + str(i + 1) for i in range(0, prefix_length)] + ['label']

