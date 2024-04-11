import random
import json
import os
from utils.generate_condition import *
from utils.table_wrapper import WikiTable
from tqdm import tqdm
import warnings
import multiprocessing as mp
warnings.filterwarnings("ignore")


def generate_conjunction_fact(table_data, fact_template):
    '''
    "fact_template": "The [target_col] that have [condition] are [executed_results]."
    '''

    table = WikiTable(table_data)
    
    source_cols = sample_source_cols(table, source_col_count)
    if source_cols == None:
        return None, None
    
    target_col_idx = table.key_column_idx
    target_col_name = table.header[target_col_idx]   


    
