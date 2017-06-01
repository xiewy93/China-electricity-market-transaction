# -*- coding: utf-8 -*-
"""
Created on Mon May  8 09:28:38 2017

@author: lenovo
"""

import pandas as pd
import copy 


class  trade_rules():
    
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
        self.buyer_data = buyer_data
        self.seller_data = seller_data
                        
    def compute_sum_deal_quantity(self):
        buy_sum_quantity = copy.deepcopy(list(self.buyer_data.sum_quantity))
        sell_sum_quantity = copy.deepcopy(list(self.seller_data.sum_quantity))
        
        i = j = 0
        pair  =[]
        while list(self.buyer_data.price)[i] >= list(self.seller_data.price)[j]:
            if buy_sum_quantity[i] > sell_sum_quantity[j]:
                pair.append([list(self.buyer_data.price)[i],list(self.seller_data.price)[j],sell_sum_quantity[j]])
                buy_sum_quantity[i] = buy_sum_quantity[i]-sell_sum_quantity[j]
                j = j+1
            elif buy_sum_quantity[i] < sell_sum_quantity[j]:
                pair.append([list(self.buyer_data.price)[i],list(self.seller_data.price)[j],buy_sum_quantity[i]])
                sell_sum_quantity[j] = sell_sum_quantity[j]-buy_sum_quantity[i]
                i = i+1
            else:
                pair.append([list(self.buyer_data.price)[i],list(self.seller_data.price)[j],buy_sum_quantity[i]])
                j = j+1
                i = i+1       
                
        df = pd.DataFrame(pair,columns = [self.get_buy_price,self.get_sell_price,self.get_deal_quantity])
        return df
    
    def merge_data(self,return_market_participants_data,left_on):
        df = self.compute_sum_deal_quantity()
        df = pd.merge(df, return_market_participants_data, left_on = left_on, right_on=self.get_price).drop(self.get_price, axis=1)
        return df
        
    def assign_sum_deal_quantity(self,merged_data):
        assign_quantity = []
        for i in range(len(merged_data)):
            assign_quantity.append([merged_data.deal_quantity[i]*j/sum(merged_data.quantity[i]) for j in merged_data.quantity[i]])
        merged_data[self.get_assign_quantity] = assign_quantity
        return merged_data

    def mean_voidance(self,assigned_data):
        mean_voidance_price=( (assigned_data.buy_price+assigned_data.sell_price)/2 )
        assigned_data[self.get_mean_voidance_price]=pd.Series(mean_voidance_price)  
        return assigned_data
        
    def unified_voidance(self,mean_voidance_data):
        unified_price=list(mean_voidance_data.mean_voidance_price)[-1]
        mean_voidance_data['unified_voidance']=list([unified_price for i in range(len(mean_voidance_data))])
        return mean_voidance_data
        
    def return_undeal( self,return_market_participants_data,assign_quantity_result):
        participants_data = return_market_participants_data
        participants_quantity = list(copy.deepcopy(participants_data[self.get_quantity]))
        assign_quantity = list(copy.deepcopy(assign_quantity_result.assign_quantity))
        i=j=0
        for k in range(len(assign_quantity)):
            if sum(participants_quantity[i]) > sum(assign_quantity[j]):
                participants_quantity[i] = list( map(lambda x: x[0]-x[1], zip(participants_quantity[i], assign_quantity_result.assign_quantity[j])))
                j=j+1
            else:
                 participants_quantity[i] = list( map(lambda x: x[0]-x[1], zip(participants_quantity[i], assign_quantity_result.assign_quantity[j])))
                 i=i+1
                 j=j+1
        participants_data['undeal_sum_quantity'] = list([sum(participants_quantity[i]) for i in range(len(participants_quantity))])
        participants_data['undeal_quantity'] = participants_quantity
        df=participants_data[(participants_data.undeal_sum_quantity > 0)]
        return df    
        
    def return_all_results(self):
        compute_sum_deal_quantity = self.compute_sum_deal_quantity()
        buy_deal_data, sell_deal_data = self.merge_data(self.buyer_data,self.get_buy_price) , self.merge_data(self.seller_data,self.get_sell_price)
        assign_buy_quantity_result , assign_sell_quantity_result = self.assign_sum_deal_quantity(buy_deal_data) , self.assign_sum_deal_quantity(sell_deal_data)        
        buyer_mean_voidance_result , seller_mean_voidance_result = self.mean_voidance(assign_buy_quantity_result) , self.mean_voidance(assign_sell_quantity_result)
        buyer_unified_voidance_result , seller_unified_voidance_result = self.unified_voidance(buyer_mean_voidance_result) , self.unified_voidance(seller_mean_voidance_result)      
        buyer_undeal_results , seller_undeal_results = self.return_undeal(self.buyer_data,assign_buy_quantity_result) , self.return_undeal(self.seller_data,assign_sell_quantity_result)
        
        
        all_results = {}
        all_results['compute_sum_deal_quantity'] = compute_sum_deal_quantity
        all_results['buy_deal_data'] = buy_deal_data
        all_results['sell_deal_data'] = sell_deal_data
        all_results['assign_buy_quantity_result' ] = assign_buy_quantity_result
        all_results['assign_sell_quantity_result' ] = assign_sell_quantity_result
        all_results['buyer_mean_voidance_result' ] = buyer_mean_voidance_result
        all_results['seller_mean_voidance_result' ] = seller_mean_voidance_result
        all_results['buyer_unified_voidance_result' ] = buyer_unified_voidance_result
        all_results['seller_unified_voidance_result' ] = seller_unified_voidance_result
        all_results['buyer_undeal_results' ] = buyer_undeal_results
        all_results['seller_undeal_results' ] = seller_undeal_results

        return all_results