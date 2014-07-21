from __future__ import division

import pandas as pd
import numpy as np

from edge import Edge

def calc_wtd_ctime():
    # Assumes that file is in current directory
    filename = r'jobs.txt'
    
    jobs_df = pd.read_csv(filename, sep=" ", 
                          header=0, 
                          names=['weight', 'length'])
    jobs_df['diff'] = jobs_df['weight'] - jobs_df['length']
    jobs_df['ratio'] = jobs_df['weight']/jobs_df['length']
    
    
    # Want to sort jobs in decreasing order of 'weight-length' and, after that,
    # descreasing weight
    sorted_df = jobs_df.sort(['diff', 'weight'], ascending=[0,0])
    
    # Completion time for each job in the schedule is the cumulative sum of elapsed
    # time for prior jobs and the job in question
    sorted_df['c_time'] = sorted_df['length'].cumsum()

    # Print weighted sum of completion time
    print np.sum(sorted_df['weight']*sorted_df['c_time'])
    
    sorted_df = jobs_df.sort(['ratio', 'weight'], ascending=[0,0])
    
    sorted_df['c_time'] = sorted_df['length'].cumsum()
    
    print 'Wtd sum of completion time (ratio): ', np.sum(sorted_df['weight']*sorted_df['c_time'])

def calc_mst_cost():
    # Assumes that file is in current directory
    filename = r'edges.txt'

    edges_df = pd.read_csv(filename, sep=" ",
                           header=0,
                           names=['v1', 'v2', 'cost'])

    vertices = pd.concat([edges_df['v1'], 
                          edges_df['v2']]).unique()

    init_vert = np.random.choice(vertices)
    # init_vert = 1

    vertices = set(vertices)

    print 'Initial vertex is', init_vert

    v_new = set([init_vert])
    e_new = set([])

    while v_new != vertices:
        query_df = edges_df[(edges_df.v1.isin(v_new) & ~edges_df.v2.isin(v_new)) | 
                            (edges_df.v2.isin(v_new) & ~edges_df.v1.isin(v_new))]
        sorted_q_df = query_df.sort(['cost'])
        
        try:
            row_to_add = sorted_q_df.iloc[0]
            vertex_to_add = (row_to_add['v1'] 
                             if row_to_add['v1'] not in v_new 
                             else row_to_add['v2'])
            edge_to_add = edge(row_to_add['v1'],
                               row_to_add['v2'],
                               row_to_add['cost'])
        
            e_new.add(edge_to_add)
            v_new.add(vertex_to_add)

        except IndexError:
            print 'Query for v1 in v_new and v2 not in v_new returned no results.'
    
    total_cost = 0
    for e in e_new:
        total_cost += e.cost
    
    print 'Cost of spanning tree:', total_cost
if __name__ == '__main__':
    calc_wtd_ctime()
    calc_mst_cost()
