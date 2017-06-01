# -*- coding: utf-8 -*-
"""
Created on Fri May 19 09:35:48 2017

@author: lenovo
"""

import init_market_participants

class  set_seller(init_market_participants.init_market_participants):
        
    def return_seller_data(self):
        seller_data = init_market_participants.init_market_participants.return_init_participants_data(self,ascending=True)
        return seller_data