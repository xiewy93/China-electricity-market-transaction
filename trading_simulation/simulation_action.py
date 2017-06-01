# -*- coding: utf-8 -*-
"""
Created on Wed May  3 11:51:17 2017

@author: lenovo
"""

import pandas as pd
import scipy.stats as stats


class  simulation_action():
        
    
    def __init__(self,package_num,simulation_ways):
        self.package_num = package_num
        self.simulation_ways = simulation_ways

    def sampling_ways(self,simulation_ways):
        if self.simulation_ways == ' uniform ':
            Upper_limit = int(input('Upper_limit = '))
            Down_limit = int(input('Down_limit = '))
            return  pd.Series(stats.uniform.rvs(Upper_limit,Down_limit,size=self.package_num))
        
        elif self.simulation_ways ==' normal ':
            mean = int(input('mean = '))
            var = int(input('var = '))
            return  pd.Series(stats.norm.rvs(mean,var,size=self.package_num))
        
        elif self.simulation_ways ==' exponential ':
            lamda = int(input('lamda = '))
            return  pd.Series(stats.expon.rvs(scale=1 /lamda,size=self.package_num))
        
        
      
        