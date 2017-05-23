#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:
# Linwood Creekmore
# Email: valinvescap@gmail.com

import pandas as pd
import numpy as np
from multiprocessing import Pool, cpu_count
from concurrent.futures import ProcessPoolExecutor
from .helpers import shaper
import argparse

cores = cpu_count()
e = ProcessPoolExecutor(max_workers=cores)

def call_apply_fn(df):
    return df.apply(shaper, axis=1)

def parallelize_dataframe(df):
    """Applying function"""
    df_split = np.array_split(df, cores*2)
    finaldf = pd.concat(list(e.map(call_apply_fn, df_split)))
    return finaldf
#
# if __name__ == '__main__':
#     import sys
#     parallelize_dataframe(sys.argv[1:])
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parallelize pandas apply function')
    parser.add_argument('--df', metavar='pandas.core.frame.DataFrame', required=True,
                        help='The target dataframe to apply the function.')
    parser.add_argument('--func', metavar='function', required=False,
                        help='The function to be applied to the dataframe.')
    args = parser.parse_args()
    model_schema(df=args.df, func=args.func)


