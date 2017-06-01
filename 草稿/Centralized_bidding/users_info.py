# -*- coding: utf-8 -*-
"""
Created on Mon May 15 09:06:22 2017

@author: lenovo
"""
import pandas as pd
import scipy.stats as stats
import simulation_action

class  users_info(simulation_action.simulation_action):
    get_user_name = 'user_'
    get_user_id = 'user_id' 
    get_assigned_sum_quantity = 'assigned_sum_quantity'
    get_sum_quantity = 'sum_quantity'
    get_assigned_price = 'assigned_price'
    
    def __init__(self,sell_num,buy_num,user_type,package_num,simulation_ways):
        self.sell_num = sell_num
        self.buy_num = buy_num
        self.user_type = user_type
        simulation_action.simulation_action.__init__(self,package_num,simulation_ways)
        
    def set_quantity(self,user_num):
        assigned_sum_quantity = []
        sum_quantity = []
        user_id = [self.get_user_name+str(i+1) for i in range(user_num)]
        random_variable_samples = self.sampling_ways(self.simulation_ways)
        for i in range(user_num):
            new = [round(j)*1000 for j in random_variable_samples]
            sum_new = sum(new)
            assigned_sum_quantity.append(new)
            sum_quantity.append(sum_new)
            
        df=pd.DataFrame({self.get_user_id:user_id, self.get_assigned_sum_quantity:assigned_sum_quantity, self.get_sum_quantity:sum_quantity}, columns=[self.get_user_id,self.get_assigned_sum_quantity,self.get_sum_quantity]) 
        return df
        
    def set_assigned_price(self,user_num):
        hydroelectricity_price=0.288
        routine_transactions_floating_price=0.15
        routine_translation_transactions_floating_price=0.05
        precision_support_transactions_floating_price=0.3
        precision_translation_transactions_floating_price=0.09
        
        assigned_price = []
        df = self.set_quantity(user_num)
        
        if self.user_type == 'routine_transactions':
            for i in range(user_num):
                new = [round(j,3) for j in pd.Series(stats.uniform.rvs(hydroelectricity_price*(1-routine_transactions_floating_price),hydroelectricity_price*(1+routine_transactions_floating_price),size=self.package_num))]
                assigned_price.append(new)
        elif self.user_type == 'routine_translation_transactions':
            for i in range(user_num):
                new = [round(j,3) for j in pd.Series(stats.uniform.rvs(hydroelectricity_price-routine_translation_transactions_floating_price,hydroelectricity_price+routine_translation_transactions_floating_price,size=self.package_num))]
                assigned_price.append(new)
        elif self.user_type == 'precision_support_transactions':
            for i in range(user_num):
                new = [round(j,3) for j in pd.Series(stats.uniform.rvs(hydroelectricity_price*(1-precision_support_transactions_floating_price),hydroelectricity_price*(1+precision_support_transactions_floating_price),size=self.package_num))]
                assigned_price.append(new)
        elif self.user_type == 'precision_translation_transactions':
             for i in range(user_num):
                new = [round(j,3) for j in pd.Series(stats.uniform.rvs(hydroelectricity_price-precision_translation_transactions_floating_price,hydroelectricity_price+precision_translation_transactions_floating_price,size=self.package_num))]
                assigned_price.append(new)
                
        df[self.get_assigned_price]=assigned_price
        return df
        
    def uniform_data_forms(self,user_num):    
        df=self.set_assigned_price(user_num)
        df_2=[]
        for i in range(len(df)):
            for j in range(len(df.ix[i,1])):
                df_2.append([df.ix[i,0],df.ix[i,3][j],df.ix[i,1][j]])
                
        df_2=pd.DataFrame(df_2)                
        return df_2
     
    def return_data(self):
        buyer = self.uniform_data_forms(self.buy_num)
        buyer.columns=['userid','price','quantity']

        seller = self.uniform_data_forms(self.sell_num)
        seller.columns=['userid','price','quantity']
        return buyer,seller

        
