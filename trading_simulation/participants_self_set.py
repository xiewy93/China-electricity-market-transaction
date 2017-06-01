# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 09:17:24 2017

@author: lenovo
"""

import pandas as pd

class participants_self_set():
    
    get_user_id = 'user_id'
    get_price = 'price'
    get_quantity = 'quantity'
    
    def __init__(self,package_num):
        self.package_num = package_num
    
    def init_participants_info(self):
        participants_type = str(input('participants_type = '))
        participants_id = str(input('participants_id = '))
        participants_info = []
        print("please input your price and electricity packs %d times" % (self.package_num))
        for i in range(1,self.package_num+1):
            print("please input the No.%d price and electricity packs" % (i))
            participants_set_price = int(input('price = '))
            participants_set_electricity_packs = int(input('electricity_packs = '))
            participants_info.append([participants_id, participants_set_price, participants_set_electricity_packs])
        
        df = pd.DataFrame(participants_info, columns=[self.get_user_id,self.get_price,self.get_quantity])    
        return df
        
    