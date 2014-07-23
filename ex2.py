#!/usr/bin/env python

from __future__ import division

import pandas as pd
import numpy as np

from itertools import izip
from edge import Edge
from union_find import UnionFind

# Number of clusters
K = 4

def hamming_dist(s1, s2):
    return np.sum([c1 != c2 for c1, c2 in izip(s1, s2)])

def one():
    mst = set([])
    edge_df = pd.read_csv('clustering1.txt',
                          sep=" ",
                          header=0,
                          names=['v1','v2','cost'])
    
    # Sort in order of least cost
    edge_df.sort(['cost'], inplace=True)
    edge_df.index = range(1,len(edge_df)+1)

    # The unique set of vertices...
    vertices = pd.concat([edge_df['v1'], 
                          edge_df['v2']]).unique()

    # Initialize the UnionFind structure with
    # unmerged set of unique vertices
    uf = UnionFind(vertices)

    # Iterate through Kruskal's until the number
    # of groups in the UnionFind struct is K
    it = edge_df.iterrows()
    while uf.numleaders() > K:
        rec = next(it)[1]
        v1 = rec['v1']
        v2 = rec['v2']
        cost = rec['cost']

        edge = Edge(v1, v2, cost)
        v1_lead = uf[v1]
        v2_lead = uf[v2]
        if v1_lead != v2_lead:
            uf.union(v1, v2)
            mst.add(edge)

    # Now iterate to the next edge that would be added 
    # to form the K-1th cluster
    cond = True
    while cond:
        rec = next(it)[1]
        v1 = rec['v1']
        v2 = rec['v2']
        cost = rec['cost']
        
        edge = Edge(v1, v2, cost)
        v1_lead = uf[v1]
        v2_lead = uf[v2]
        cond = (v1_lead == v2_lead)
        if not cond:
            mks = cost

    return mks

def strip(text):
    try:
        return text.replace(" ","")
    except AttributeError:
        return text

def two():
    """ 
    Calculates largest value k such that there is a k-clustering
    with spacing >= 3
    """
    vert_df = pd.read_csv('clustering_big.txt',
                          header=0,
                          names=['vid'],
                          converters = {'vid' : strip})
                          
    
if __name__ == '__main__':
    mks = one()
    two()
    print mks