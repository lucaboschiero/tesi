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

class Encoding: 
    def __init__(self, log: DataFrame = None, labeling= None):
        self.CONF = {  # This contains the configuration for the run
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

        self.df = TRACE_TO_DF[self.CONF['feature_selection']](
            log,
            prefix_length=self.CONF['prefix_length'],
            padding=self.CONF['padding'],
            prefix_length_strategy=self.CONF['prefix_length_strategy'],
            labeling_type=self.CONF['labeling_type'],
            generation_type=self.CONF['task_generation_type'],
            feature_list=train_cols,
            #target_event=CONF['target_event']
        )

        self.encoder = Encoder(df=self.df, attribute_encoding=self.CONF['attribute_encoding'])

    def encode_traces(self):
        
        self.encoder.encode(df=self.df)
        #print(df)

        features = []
        encoded_data = []
        labels = []
        column_names = list(self.df.columns[0:4])
        for index, row in self.df.iterrows():  
            labels.append(row['label'] -1)
            encoded_data.append(list(row[0:4]))  
        if not features:
            features = list(column_names)
            
        #print("Encoded data: ",encoded_data)
        #print("Features: ",features)
        #print(encoded_data)
        #print("Labels: ",labels)
        return DTInput(features, encoded_data, labels)
    
    def decode_traces(self, log):
        df_input = pd.DataFrame({'prefix_1': [log[0]], 'prefix_2': [log[1]], 'prefix_3': [log[2]]})
        self.encoder.decode(df=df_input)
        return df_input
        
