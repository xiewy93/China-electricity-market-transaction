# -*- coding: utf-8 -*-
"""
Created on Mon May  8 09:28:38 2017

@author: lenovo
"""
from set_buyer import set_buyer
from set_seller import set_seller
from trade_rules import trade_rules
from start_trading import start_trading
#from init_market_participants import init_market_participants

if __name__=='__main__':
    seller_num,buyer_num,package_num =10,8,3
    user_type = 'routine_transactions'
    simulation_ways = ' uniform '
    
#    test = init_market_participants(buyer_num,user_type,package_num,simulation_ways) 
#    df = test.uniform_data_forms()
    
    pre_buyer = set_buyer(buyer_num,user_type,package_num,simulation_ways) 
    buyer = pre_buyer.return_buyer_data()
    
    pre_seller = set_seller(seller_num,user_type,package_num,simulation_ways) 
    seller = pre_seller.return_seller_data()

    trade_action = trade_rules(buyer,seller)
    trade_rules_results = trade_action.return_all_results()

    start_trading_action = start_trading(buyer,seller)
    start_trading_action.get_picture()