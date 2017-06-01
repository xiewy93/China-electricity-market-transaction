# -*- coding: utf-8 -*-
"""
Created on Mon May 15 09:06:22 2017

@author: lenovo
"""
import pandas as pd
import scipy.stats as stats
import simulation_action

class  init_market_participants(simulation_action.simulation_action):
    get_user_name = 'user_'
    get_user_id = 'user_id'
    get_quantity = 'quantity'
    get_price = 'price'
    get_user_counts = 'user_count'
    get_assigned_sum_quantity = 'assigned_sum_quantity'
    get_sum_quantity = 'sum_quantity'
    get_assigned_price = 'assigned_price'
    
    def __init__(self,participants_num,participants_type,package_num,simulation_ways):
        self.participants_num = participants_num
        self.participants_type = participants_type
        simulation_action.simulation_action.__init__(self,package_num,simulation_ways)
        
    def set_quantity(self):
        assigned_sum_quantity = []
        sum_quantity = []
        user_id = [self.get_user_name+str(i+1) for i in range(self.participants_num)]
        random_variable_samples = self.sampling_ways(self.simulation_ways)
        for i in range(self.participants_num):
            new = [round(j)*1000 for j in random_variable_samples]
            sum_new = sum(new)
            assigned_sum_quantity.append(new)
            sum_quantity.append(sum_new)
            
        df=pd.DataFrame({self.get_user_id:user_id, self.get_assigned_sum_quantity:assigned_sum_quantity, self.get_sum_quantity:sum_quantity}, columns=[self.get_user_id,self.get_assigned_sum_quantity,self.get_sum_quantity]) 
        return df
    
    def set_assigned_price(self):
        hydroelectricity_price=0.288
        routine_transactions_floating_price=0.15
        routine_translation_transactions_floating_price=0.05
        precision_support_transactions_floating_price=0.3
        precision_translation_transactions_floating_price=0.09
        
        assigned_price = []
        df = self.set_quantity()
        
        if self.participants_type == 'routine_transactions':
            for i in range(self.participants_num):
                new = [round(j,3) for j in pd.Series(stats.uniform.rvs(hydroelectricity_price*(1-routine_transactions_floating_price),hydroelectricity_price*(1+routine_transactions_floating_price),size=self.package_num))]
                assigned_price.append(new)
        elif self.participants_type == 'routine_translation_transactions':
            for i in range(self.participants_num):
                new = [round(j,3) for j in pd.Series(stats.uniform.rvs(hydroelectricity_price-routine_translation_transactions_floating_price,hydroelectricity_price+routine_translation_transactions_floating_price,size=self.package_num))]
                assigned_price.append(new)
        elif self.participants_type == 'precision_support_transactions':
            for i in range(self.participants_num):
                new = [round(j,3) for j in pd.Series(stats.uniform.rvs(hydroelectricity_price*(1-precision_support_transactions_floating_price),hydroelectricity_price*(1+precision_support_transactions_floating_price),size=self.package_num))]
                assigned_price.append(new)
        elif self.participants_type == 'precision_translation_transactions':
             for i in range(self.participants_num):
                new = [round(j,3) for j in pd.Series(stats.uniform.rvs(hydroelectricity_price-precision_translation_transactions_floating_price,hydroelectricity_price+precision_translation_transactions_floating_price,size=self.package_num))]
                assigned_price.append(new)
                
        df[self.get_assigned_price]=assigned_price
        return df
        
    def uniform_data_forms(self):    
        df = self.set_assigned_price()
        df_2 = []
        for i in range(len(df)):
            for j in range(len(df.ix[i,1])):
                df_2.append([df.ix[i,0],df.ix[i,3][j],df.ix[i,1][j]])
                
        df_2 = pd.DataFrame(df_2)
        df_2.columns=[self.get_user_id,self.get_price,self.get_quantity]                
        return df_2
        
    def get_append(self,input_data):
        temp = []
        temp2 = []
        for i in input_data[self.get_user_id]:
            temp.append(i)
        for j in input_data[self.get_quantity]:
            temp2.append(j)
        return temp,temp2    
        
    def return_init_participants_data(self,ascending):
        uniformed_data = self.uniform_data_forms()
        self.df = uniformed_data.price.abs()
        self.df = uniformed_data.groupby(self.get_price).agg(lambda x:self.get_append(x))
        self.df[self.get_user_counts] = uniformed_data.groupby(self.get_price)[self.get_quantity].count()
        self.df[self.get_sum_quantity] = uniformed_data.groupby(self.get_price)[self.get_quantity].sum()
        self.df = self.df.reset_index()
        self.df = self.df.sort_values(self.get_price,ascending = ascending)
        df = pd.DataFrame(self.df)
        colnames = [self.get_price,self.get_user_id,self.get_quantity,self.get_user_counts,self.get_sum_quantity]
        df.columns = colnames
        return df 


        
