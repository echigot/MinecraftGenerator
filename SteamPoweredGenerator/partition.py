# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 13:09:56 2019

@author: echigot
"""

import operator
import math
import utilityFunctions as uf
import numpy as np
import random as rd


buildable = False

class Partition :
    
    def __init__(self, x, y, z, width, height, length):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.length = length
        
    
    def isBuildable():
        pass