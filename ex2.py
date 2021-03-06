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

def hamming_dist2(s1, s2):
    return bin(int(s1,2) ^ int(s2,2)).count("1")

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

def nearby(v, v_set):
    """
    Returns the subset of v_set that are within a Hamming distance
    of 2 or less
    """
    to_return = set([])
    for other_v in v_set:
        if hamming_dist2(v, other_v) <= 2:
            to_return.add(other_v)
    
    return to_return

def two():
    """ 
    Calculates largest value k such that there is a k-clustering
    with spacing >= 3
    """
    
    # Read in the file, converting to str of binary number
    vert_df = pd.read_csv('clustering_big.txt',
                          header=0,
                          names=['vid'],
                          converters = {'vid' : strip})
    
    vertices = vert_df['vid'].unique()
    uf = UnionFind(vertices)
    to_visit = set(vertices)

    # 
    while len(to_visit) > 0:
        # Every iteration of the while loop corresponds to 
        # pulling off a new vertex label and attempting to merge
        # with all other vertices connected at cost <= 2
        this_v = to_visit.pop()

        nearby_v = nearby(this_v, to_visit)

        for v in nearby_v:
            l1 = uf[this_v]
            l2 = uf[v]
            if l1 != l2:
                uf.union(this_v, v)
                to_visit.remove(v)

    return uf.numleaders()
        
if __name__ == '__main__':
    mks = one()
    n_clust = two()
    print mks
    print n_clust
