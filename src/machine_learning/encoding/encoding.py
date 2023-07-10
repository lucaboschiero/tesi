from src.constants import *
from src.machine_learning.labeling import *
from src.models.DTInput import *
from src.enums.ConstraintChecker import *
import settings
from src.machine_learning.label.common import LabelTypes
from pandas import DataFrame
from src.machine_learning.encoding.constants import EncodingType
from src.machine_learning.encoding.feature_encoder.frequency_features import frequency_features
from src.machine_learning.encoding.feature_encoder.simple_features import simple_features
from src.machine_learning.encoding.feature_encoder.complex_features import complex_features
from src.machine_learning.encoding.data_encoder import *

TRACE_TO_DF = {
    EncodingType.SIMPLE.value : simple_features,
    EncodingType.FREQUENCY.value : frequency_features,
    EncodingType.COMPLEX.value : complex_features,
    # EncodingType.DECLARE.value : declare_features
}

def encode_traces(log, frequent_events, frequent_pairs, checkers, rules, labeling):

    event_checkers = list(filter(lambda checker: checker in [ConstraintChecker.EXISTENCE, ConstraintChecker.ABSENCE, ConstraintChecker.INIT, ConstraintChecker.EXACTLY], checkers))
    pair_checkers = list(filter(lambda checker: checker not in [ConstraintChecker.EXISTENCE, ConstraintChecker.ABSENCE, ConstraintChecker.INIT, ConstraintChecker.EXACTLY], checkers))
    
    CONF = {  # This contains the configuration for the run
                'data': log,
                'prefix_length_strategy': 'fixed',
                'prefix_length': 3,
                'padding': True,  # TODO: why use of padding?
                'feature_selection': 'simple',
                'task_generation_type': 'all_in_one',
                'attribute_encoding': 'label',  # LABEL
                'labeling_type': LabelTypes.ATTRIBUTE_STRING,
    }
    train_cols: DataFrame=None

    df = TRACE_TO_DF[CONF['feature_selection']](
        log,
        prefix_length=CONF['prefix_length'],
        padding=CONF['padding'],
        prefix_length_strategy=CONF['prefix_length_strategy'],
        labeling_type=CONF['labeling_type'],
        generation_type=CONF['task_generation_type'],
        feature_list=train_cols,
        #target_event=CONF['target_event']
    )

    encoder = Encoder(df=df, attribute_encoding=CONF['attribute_encoding'])

    features = []
    encoded_data = []
    
    for trace in log:
        encoder.encode(df=trace)
        trace_result = {}
        for a in frequent_events:
            for checker in event_checkers:
                key = checker.value + "[" + a + "]"
                trace_result[key] = trace
        for (a, b) in frequent_pairs:
            for checker in pair_checkers:
                key = checker.value + "[" + a + "," + b +"]"
                trace_result[key] = trace
        if not features:
            features = list(trace_result.keys())
        encoded_data.append(list(trace_result.values()))
        #print("Encoded data: ",encoded_data)
    labels = generate_labels(log, labeling)
    return DTInput(features, encoded_data, labels)
