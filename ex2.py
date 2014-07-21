#!/usr/bin/env python

from __future__ import division

import pandas as pd
import numpy as np

from edge import Edge

# Number of clusters
K = 4

def one():
    edge_df = pd.read_csv('clustering1.txt',
                          sep=" ",
                          header=0,
                          names=['v1','v2','cost'])
    
    # Sort in order of least cost
    edge_df.sort(['cost'])

def two():
    pass

if __name__ == '__main__':
    pass
