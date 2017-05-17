# -*- coding: utf-8 -*-
"""
Created on Mon May  8 09:28:38 2017

@author: lenovo
"""

from users_info import users_info
from trade_rules import trade_rules

if __name__=='__main__':
    sell_num,buy_num,package_num =10,8,3
    user_type = 'routine_transactions'
    simulation_ways = ' uniform '
    
    pre_action = users_info(sell_num,buy_num,user_type,package_num,simulation_ways) 
    buyer,seller = pre_action.return_data()

    trade_action = trade_rules(buyer,seller)
    df = trade_action.return_all_results()
    trade_action.get_picture() 