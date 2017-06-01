# -*- coding: utf-8 -*-
"""
Created on Fri May 19 09:40:14 2017

@author: lenovo
"""

import matplotlib.pyplot as plt
from trade_rules import trade_rules

class  start_trading(trade_rules):
    
    get_id = 'userid'
    get_quantity = 'quantity'
    get_price = 'price'
    get_user_counts = 'user_count'
    get_sum_quantity = 'sum_quantity'
    get_buy_price = 'buy_price'
    get_sell_price = 'sell_price'
    get_deal_quantity = 'deal_quantity'
    get_assign_quantity = 'assign_quantity'
    get_mean_voidance_price = 'mean_voidance_price'    
    
    def __init__(self, buyer_data, seller_data):
        trade_rules.__init__(self,buyer_data, seller_data)
        
    def input_trade_rules(self):
        trade_rules_results = trade_rules.trade_rules.return_all_results()
        return trade_rules_results
                  
    def pre_data_for_picture(self,return_market_participants_data):
        price=list(return_market_participants_data.price)
        price.insert(0,0)
        sum_quantity = return_market_participants_data.sum_quantity
        picture_data = [sum(sum_quantity[:i]) for i in range(len(sum_quantity)+1)]
        return picture_data , price
        
    def get_picture(self):
        x, buy_price = self.pre_data_for_picture(self.buyer_data) 
        y, sell_price = self.pre_data_for_picture(self.seller_data)
        plt.plot(x, buy_price, linestyle=':', drawstyle='steps')
        plt.plot(y, sell_price, linestyle='--', drawstyle='steps')
        plt.xlim(0.0, max(x[-1],y[-1]))
        return plt.show()
    
    def return_all_results(self):
        return self.input_trade_rules()
        
           

#if __name__=='__main__':
#    input_sell=pd.DataFrame(
#                [['sell_3',-0.26,250],
#                ['sell_2',-0.25,400],
#                ['sell_3',-0.25,300],
#                ['sell_1',-0.24,200],
#                ['sell_2',-0.24,300],
#                ['sell_1',-0.23,100]])
#    input_sell.columns=['userid','price','quantity']
#    input_buy=pd.DataFrame(
#            [['buy_3',-0.26, 250],
#            ['buy_2',-0.25, 400],
#            ['buy_3',-0.25, 300],
#            ['buy_1',-0.24, 200],
#            ['buy_2',-0.24, 300],
#            ['buy_1',-0.23, 100]])
#    input_buy.columns=['userid','price','quantity']
#
#       
#    pre_action = trade_rules(input_sell,input_buy)
#    df = pre_action.return_all_results()
#    pre_action.get_picture() 