# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 13:18:30 2019

@author: echigot
"""

import operator
import math
import utilityFunctions as uf
import numpy as np
import random as rd
import partitionning as part
import partition


partitions

def perform(level, box, options):
    #main program
    
    global partitions
    partitions = part.binarySpacePartitioning()
    
    for p in partitions:
        pass