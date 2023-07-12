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

def encode_traces(log, labeling):
    
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
    encoder.encode(df=df)
    #print(df)

    features = []
    encoded_data = []
    labels = []
    column_names = list(df.columns[0:4])
    for index, row in df.iterrows():  
        labels.append(row['label'] -1)
        encoded_data.append(list(row[0:4]))  
    if not features:
        features = list(column_names)
        
    #print("Encoded data: ",encoded_data)
    #print("Features: ",features)
    #print(encoded_data)
    #print("Labels: ",labels)
    return DTInput(features, encoded_data, labels)
