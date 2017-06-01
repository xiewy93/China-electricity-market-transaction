# -*- coding: utf-8 -*-
"""
Created on Mon May  8 09:28:38 2017

@author: lenovo
"""

import pandas as pd
import copy 
import matplotlib.pyplot as plt


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
    
    def __init__(self,input_sell,input_buy):
        self.input_sell=input_sell
        self.input_buy = input_buy
        
        
    def get_append(self,input_data):
        temp=[]
        temp2=[]
        for i in input_data[self.get_id]:
            temp.append(i)
        for j in input_data[self.get_quantity]:
            temp2.append(j)
        return temp,temp2   
        
    def init_participants(self,input_buy,ascending):
        self.df = input_buy.price.abs()
        self.df = input_buy.groupby(self.get_price).agg(lambda x:self.get_append(x))
        self.df[self.get_user_counts] = input_buy.groupby(self.get_price)[self.get_quantity].count()
        self.df[self.get_sum_quantity] = input_buy.groupby(self.get_price)[self.get_quantity].sum()
        self.df = self.df.reset_index()
        self.df = self.df.sort_values(self.get_price,ascending=ascending)
        df = pd.DataFrame(self.df)
        colnames = [self.get_price,self.get_id,self.get_quantity,self.get_user_counts,self.get_sum_quantity]
        df.columns = colnames
        return df
            
    def pre_data(self):
        buy = self.init_participants(self.input_buy,False)
        sell = self.init_participants(self.input_sell,True)
        return buy,sell
                            
    def compute_sum_deal_quantity(self):
        df_buy,df_sell = self.pre_data()
        buy_sum_quantity = copy.deepcopy(list(df_buy.sum_quantity))
        sell_sum_quantity = copy.deepcopy(list(df_sell.sum_quantity))
        
        i = j = 0
        pair  =[]
        while list(df_buy.price)[i] >= list(df_sell.price)[j]:
            if buy_sum_quantity[i] > sell_sum_quantity[j]:
                pair.append([list(df_buy.price)[i],list(df_sell.price)[j],sell_sum_quantity[j]])
                buy_sum_quantity[i] = buy_sum_quantity[i]-sell_sum_quantity[j]
                j = j+1
            elif buy_sum_quantity[i] < sell_sum_quantity[j]:
                pair.append([list(df_buy.price)[i],list(df_sell.price)[j],buy_sum_quantity[i]])
                sell_sum_quantity[j] = sell_sum_quantity[j]-buy_sum_quantity[i]
                i = i+1
            else:
                pair.append([list(df_buy.price)[i],list(df_sell.price)[j],buy_sum_quantity[i]])
                j = j+1
                i = i+1       
                
        df = pd.DataFrame(pair,columns = [self.get_buy_price,self.get_sell_price,self.get_deal_quantity])
        return df
    
    def merge_data(self,pre_data,left_on):
        df = self.compute_sum_deal_quantity()
        df = pd.merge(df, pre_data, left_on = left_on, right_on=self.get_price).drop(self.get_price, axis=1)
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
        
        
    def return_undeal( self,pre_data,assign_quantity_result):
        participants_data = pre_data
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
        
   
       
    def pre_data_for_picture(self,pre_data):
        price=list(pre_data.price)
        price.insert(0,0)
        sum_quantity = pre_data.sum_quantity
        picture_data = [sum(sum_quantity[:i]) for i in range(len(sum_quantity)+1)]
        return picture_data , price
        
    def get_picture(self):
        x, buy_price = self.pre_data_for_picture(self.init_participants(self.input_buy,False)) 
        y, sell_price = self.pre_data_for_picture(self.init_participants(self.input_sell,True))
        plt.plot(x, buy_price, linestyle=':', drawstyle='steps')
        plt.plot(y, sell_price, linestyle='--', drawstyle='steps')
        plt.xlim(0.0, max(x[-1],y[-1]))
        return plt.show()
    
    def return_all_results(self):
        buy,sell = self.pre_data()
        compute_sum_deal_quantity = self.compute_sum_deal_quantity()
        buy_deal_data, sell_deal_data = self.merge_data(buy,self.get_buy_price) , self.merge_data(sell,self.get_sell_price)
        assign_buy_quantity_result , assign_sell_quantity_result = self.assign_sum_deal_quantity(buy_deal_data) , self.assign_sum_deal_quantity(sell_deal_data)        
        buyer_mean_voidance_result , seller_mean_voidance_result = self.mean_voidance(assign_buy_quantity_result) , self.mean_voidance(assign_sell_quantity_result)
        buyer_unified_voidance_result , seller_unified_voidance_result = self.unified_voidance(buyer_mean_voidance_result) , self.unified_voidance(seller_mean_voidance_result)      
        return_buyer_undeal , return_seller_undeal = self.return_undeal(buy,assign_buy_quantity_result) , self.return_undeal(sell,assign_sell_quantity_result)
        
        
        all_results = {}
        all_results['buy'] = buy
        all_results['sell'] = sell
        all_results['compute_sum_deal_quantity'] = compute_sum_deal_quantity
        all_results['buy_deal_data'] = buy_deal_data
        all_results['sell_deal_data'] = sell_deal_data
        all_results['assign_buy_quantity_result' ] = assign_buy_quantity_result
        all_results['assign_sell_quantity_result' ] = assign_sell_quantity_result
        all_results['buyer_mean_voidance_result' ] = buyer_mean_voidance_result
        all_results['seller_mean_voidance_result' ] = seller_mean_voidance_result
        all_results['buyer_unified_voidance_result' ] = buyer_unified_voidance_result
        all_results['seller_unified_voidance_result' ] = seller_unified_voidance_result
        all_results['return_buyer_undeal' ] = return_buyer_undeal
        all_results['return_seller_undeal' ] = return_seller_undeal
        return all_results
        
        

   

if __name__=='__main__':
    input_sell=pd.DataFrame(
                [['sell_3',-0.26,250],
                ['sell_2',-0.25,400],
                ['sell_3',-0.25,300],
                ['sell_1',-0.24,200],
                ['sell_2',-0.24,300],
                ['sell_1',-0.23,100]])
    input_sell.columns=['userid','price','quantity']
    input_buy=pd.DataFrame(
            [['buy_3',-0.26, 250],
            ['buy_2',-0.25, 400],
            ['buy_3',-0.25, 300],
            ['buy_1',-0.24, 200],
            ['buy_2',-0.24, 300],
            ['buy_1',-0.23, 100]])
    input_buy.columns=['userid','price','quantity']

       
    pre_action = trade_rules(input_sell,input_buy)
    df = pre_action.return_all_results()
    pre_action.get_picture() 