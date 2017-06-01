# -*- coding: utf-8 -*-
"""
Created on Fri May 19 09:32:31 2017

@author: lenovo
"""
import init_market_participants

class  set_buyer(init_market_participants.init_market_participants):        
     
    def return_buyer_data(self):
        buyer_data = init_market_participants.init_market_participants.return_init_participants_data(self,ascending=False)
        return buyer_data
