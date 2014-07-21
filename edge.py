#!/usr/bin/env python

class Edge(object):
    def __init__(self, v1, v2, cost):
        self.v1 = v1
        self.v2 = v2
        self.cost = cost
    
    def __repr__(self):
        return ('v1: ' + 
                str(self.v1) + 
                ' v2: ' + 
                str(self.v2) + 
                ' cost: ' + 
                str(self.cost))

    def __eq__(self, other):
        return (self.v1 == other.v1 &
                self.v2 == other.v2 &
                self.cost == other.cost)

    def get_start_vert(self):
        return self.v1

    def get_end_vert(self):
        return self.v2
