# -*- coding: utf-8 -*-
"""
Created on Wed May  3 17:05:08 2017

@author: lenovo
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 17:58:00 2017

@author: lee
"""

#第一轮为集合竞价
#输入 list 电量+电价
#第二轮为双摘
import pandas as pd
import copy 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import scipy.stats as stats


class  set_auction():
    def __init__(self,input_sell,input_buy):
        self.input_sell=input_sell
        self.input_buy = input_buy
        
    
    def get_append(self,x):
        temp=[]
        temp2=[]
        for i in x['userid']:
            temp.append(i)
        for j in x['quantity']:
            temp2.append(j)
        return temp,temp2   
        
    def pre_data(self):
        self.df_buy=self.input_buy.price.abs()
        self.df_buy= self.input_buy.groupby('price').agg(lambda x:self.get_append(x))
        self.df_buy['count']=self.input_buy.groupby('price')['quantity'].count()
        self.df_buy['sum_quantity']=self.input_buy.groupby('price')['quantity'].sum()
        self.df_buy=self.df_buy.reset_index()
        self.df_buy=self.df_buy.sort_values('price',ascending=False)
        
        self.df_sell=self.input_sell.price.abs()
        self.df_sell = self.input_sell.groupby('price').agg(lambda x:self.get_append(x))
        self.df_sell['count']=self.input_sell.groupby('price')['quantity'].count()
        self.df_sell['sum_quantity']=self.input_sell.groupby('price')['quantity'].sum()
        self.df_sell=self.df_sell.reset_index()
        self.df_sell=self.df_sell.sort_values('price',ascending=True)
        buy_data=pd.DataFrame(self.df_buy)
        sell_data=pd.DataFrame(self.df_sell)
        buy_data.columns=['buy_price','buy_userid','buy_quantity','user_count','sum_quantity']
        sell_data.columns=['sell_price','sell_userid','sell_quantity','user_count','sum_quantity']
        return buy_data,sell_data
        
    def compute(self):
        df_buy,df_sell=self.pre_data()
        i=j=0
        pair=[]
        buy_sum_quantity=copy.deepcopy(list(df_buy.sum_quantity))
        sell_sum_quantity=copy.deepcopy(list(df_sell.sum_quantity))
        while list(df_buy.buy_price)[i]>=list(df_sell.sell_price)[j]:
            if buy_sum_quantity[i]>sell_sum_quantity[j]:
                pair.append([list(df_buy.buy_price)[i],list(df_sell.sell_price)[j],sell_sum_quantity[j]])
                buy_sum_quantity[i]=buy_sum_quantity[i]-sell_sum_quantity[j]
                j=j+1
            elif buy_sum_quantity[i]<sell_sum_quantity[j]:
                pair.append([list(df_buy.buy_price)[i],list(df_sell.sell_price)[j],buy_sum_quantity[i]])
                sell_sum_quantity[j]=sell_sum_quantity[j]-buy_sum_quantity[i]
                i=i+1
            else:
                pair.append([list(df_buy.buy_price)[i],list(df_sell.sell_price)[j],sell_sum_quantity[i]])
                j=j+1
                i=i+1       
        df=pd.DataFrame(pair,columns=['buy_price','sell_price','deal_quantity'])        
        return df

    def assign_quantity(self):
        df=self.compute()
        df_buy,df_sell=self.pre_data()
        buy_deal=pd.merge(df,df_buy,on='buy_price')
        sell_deal=pd.merge(df,df_sell,on='sell_price')
        assign_buy_quantity_result=copy.deepcopy(buy_deal[['buy_price','sell_price','deal_quantity','buy_userid']])
        assign_sell_quantity_result=copy.deepcopy(sell_deal[['buy_price','sell_price','deal_quantity','sell_userid']])
        assign_buy_quantity=[]
        assign_sell_quantity=[]
        for i in range(len(buy_deal)):
            assign_buy_quantity.append([buy_deal.deal_quantity[i]*x/sum(buy_deal.buy_quantity[i]) for x in buy_deal.buy_quantity[i]])
            assign_sell_quantity.append([sell_deal.deal_quantity[i]*x/sum(sell_deal.sell_quantity[i]) for x in sell_deal.sell_quantity[i]])
        
        assign_buy_quantity_result['assign_buy_quantity']=assign_buy_quantity
        assign_sell_quantity_result['assign_sell_quantity']=assign_sell_quantity
        return assign_buy_quantity_result,assign_sell_quantity_result
        
    def mean_voidance(self):
        buy_mean_voidance_result,sell_mean_voidance_result=self.assign_quantity()
        mean_voidance_buy_price=((buy_mean_voidance_result.buy_price+sell_mean_voidance_result.sell_price)/2)
        buy_mean_voidance_result['mean_voidance_price']=pd.Series(mean_voidance_buy_price)  
        sell_mean_voidance_result['mean_voidance_price']=pd.Series(mean_voidance_buy_price)
        return buy_mean_voidance_result,sell_mean_voidance_result
        

    def undeal(self):
        assign_buy_quantity_result,assign_sell_quantity_result=self.assign_quantity()
        buy_data,sell_data=self.pre_data()
        buy_quantity=list(copy.deepcopy(buy_data['buy_quantity']))
        i=j=0
        for k in range(len(buy_quantity)):
            if sum(buy_quantity[i])>sum(assign_buy_quantity_result.assign_buy_quantity[j]):
                buy_quantity[i]=list( map(lambda x: x[0]-x[1], zip(buy_quantity[i], assign_buy_quantity_result.assign_buy_quantity[j])))
                j=j+1
            else:
                 buy_quantity[i]=list( map(lambda x: x[0]-x[1], zip(buy_quantity[i], assign_buy_quantity_result.assign_buy_quantity[j])))
                 i=i+1
                 j=j+1
        buy_data['undeal_sum_quantity']=list([sum(buy_quantity[i]) for i in range(len(buy_quantity))])
        buy_data['undeal_quantity']=buy_quantity
        df=buy_data[(buy_data.undeal_sum_quantity > 0)]

        sell_quantity=list(copy.deepcopy(sell_data['sell_quantity']))
        i=j=0
        for k in range(len(sell_quantity)):
            if sum(sell_quantity[i])>sum(assign_sell_quantity_result.assign_sell_quantity[j]):
                sell_quantity[i]=list( map(lambda x: x[0]-x[1], zip(sell_quantity[i], assign_sell_quantity_result.assign_sell_quantity[j])))
                j=j+1
            else:
                 sell_quantity[i]=list( map(lambda x: x[0]-x[1], zip(sell_quantity[i], assign_sell_quantity_result.assign_sell_quantity[j])))
                 i=i+1
                 j=j+1
        sell_data['undeal_sum_quantity']=list([sum(sell_quantity[i]) for i in range(len(sell_quantity))])
        sell_data['undeal_quantity']=sell_quantity
        df2=sell_data[(sell_data.undeal_sum_quantity > 0)]
        return df,df2


    def return_price_margin_voidance(self):
        assign_buy_quantity_result,assign_sell_quantity_result=self.assign_quantity()
        buy_userid=list(set(list(self.input_buy.userid)))
        sell_userid=list(set(list(self.input_sell.userid)))
        Q=assign_buy_quantity_result.deal_quantity.sum()
        beta=0.25
        pair=[]
        pair2=[]
        buy_quantity=[0]*len(buy_userid)
        sell_quantity=[0]*len(sell_userid)
        buy_deal_price=[[] for i in range(len(buy_userid))]
        sell_deal_price=[[] for i in range(len(sell_userid))]
        for i in range(len(assign_buy_quantity_result)):
            pair.append([assign_buy_quantity_result.buy_userid[i],[x*assign_buy_quantity_result.buy_price[i] for x in assign_buy_quantity_result.assign_buy_quantity[i]],assign_buy_quantity_result.buy_price[i]])
            for j in range(len(buy_userid)):
               if buy_userid[j] in pair[i][0]:
                   quantity_index=pair[i][0].index(buy_userid[j])
                   buy_quantity[j]=buy_quantity[j]+pair[i][1][quantity_index]
                   buy_deal_price[j].append(pair[i][2])
                   
        for i in range(len(assign_sell_quantity_result)):
            pair2.append([assign_sell_quantity_result.sell_userid[i],[x*assign_sell_quantity_result.sell_price[i] for x in assign_sell_quantity_result.assign_sell_quantity[i]],assign_sell_quantity_result.sell_price[i]])
            for j in range(len(sell_userid)):
               if sell_userid[j] in pair2[i][0]:
                   quantity_index=pair2[i][0].index(sell_userid[j])
                   sell_quantity[j]=sell_quantity[j]+pair2[i][1][quantity_index]
                   sell_deal_price[j].append(pair2[i][2])
                   
        sell_mean_price_gap=abs(sum(sell_quantity))/Q
        buy_mean_price_gap=abs(sum(buy_quantity))/Q
        sell_deal_coefficient=(1-beta)*sell_mean_price_gap/buy_mean_price_gap+beta
        buy_deal_coefficient=beta*sell_mean_price_gap/buy_mean_price_gap+(1-beta)
        
        sell=[]
        for i in range(len(sell_deal_price)):
            a=sell_deal_price[i]
            sell.append([x*sell_deal_coefficient for x in a])
        buy=[]
        for i in range(len(buy_deal_price)):
            a=buy_deal_price[i]
            buy.append([x*buy_deal_coefficient for x in a])
        df=pd.DataFrame(buy,index=buy_userid)
        df2=pd.DataFrame(sell,index=sell_userid)
        return df,df2
    

    def unified_voidance(self):
        buy_mean_voidance_result,sell_mean_voidance_result=self.mean_voidance()
        assign_buy_quantity_result,assign_sell_quantity_result=self.assign_quantity()
        unified_price=list(buy_mean_voidance_result.mean_voidance_price)[-1]
        assign_buy_quantity_result['unified_voidance']=list([unified_price for i in range(len(assign_buy_quantity_result))])
        assign_sell_quantity_result['unified_voidance']=list([unified_price for i in range(len(assign_sell_quantity_result))])
        return assign_buy_quantity_result,assign_sell_quantity_result
        
        
      
    def get_picture(self):
        buy_data,sell_data=self.pre_data()
        buy_price=list(buy_data.buy_price)
        buy_price.insert(0,0)
        buy_sum_quantity=buy_data.sum_quantity
        sell_price=list(sell_data.sell_price)
        sell_price.insert(0,0)
        sell_sum_quantity=sell_data.sum_quantity
        x=[sum(buy_sum_quantity[:i]) for i in range(len(buy_sum_quantity)+1)]
        y=[sum(sell_sum_quantity[:i]) for i in range(len(sell_sum_quantity)+1)]
        plt.plot(x, buy_price, linestyle=':', drawstyle='steps')
        plt.plot(y, sell_price, linestyle='--', drawstyle='steps')
        plt.xlim(0.0, max(x[-1],y[-1]))
        return plt.show()

        
class  simulation_action():
    
    def __init__(self,sell_num,buy_num,user_type):
        self.sell_num = sell_num
        self.buy_num = buy_num
        self.user_type = user_type
        
    def sum_quantity(self,x):
        a=0
        b=10
        assigned_sum_quantity = []
        sum_quantity = []
        user_id = ['user_'+str(i+1) for i in range(x)]
        for i in range(x):
            new = [round(j)*1000 for j in pd.Series(stats.uniform.rvs(a,b,size=3))]
            sum_new = sum(new)
            assigned_sum_quantity.append(new)
            sum_quantity.append(sum_new)
            
        df=pd.DataFrame({'user_id':user_id,'assigned_sum_quantity':assigned_sum_quantity,'sum_quantity':sum_quantity},columns=['user_id','assigned_sum_quantity','sum_quantity']) 
        return df
        
    def assigned_price(self,x):
        assigned_price = []
        df = self.sum_quantity(x)
        if self.user_type=='routine_transactions':
            for i in range(x):
                new = [round(j,3) for j in pd.Series(stats.uniform.rvs(0.288*(1-0.15),0.288*(1+0.15),size=3))]
                assigned_price.append(new)
        elif self.user_type=='routine_translation_transactions':
            for i in range(x):
                new = [round(j,3) for j in pd.Series(stats.uniform.rvs(0.288-0.05,0.288+0.05,size=3))]
                assigned_price.append(new)
        elif self.user_type=='precision_support_transactions':
            for i in range(x):
                new = [round(j,3) for j in pd.Series(stats.uniform.rvs(0.288*(1-0.3),0.288*(1+0.3),size=3))]
                assigned_price.append(new)
        elif self.user_type=='precision_translation_transactions':
             for i in range(x):
                new = [round(j,3) for j in pd.Series(stats.uniform.rvs(0.288-0.09,0.288+0.09,size=3))]
                assigned_price.append(new)
                
        df['assigned_price']=assigned_price
        return df
        
    def uniform_forms(self,x):    
        df=self.assigned_price(x)
        df_2=[]
        for i in range(len(df)):
            for j in range(len(df.ix[i,1])):
                df_2.append([df.ix[i,0],df.ix[i,3][j],df.ix[i,1][j]])
                
        df_2=pd.DataFrame(df_2)                
        return df_2
     
    def hh(self):
        buyer = self.uniform_forms(self.buy_num)
        seller = self.uniform_forms(self.sell_num)
        return buyer,seller        

sell_num,buy_num =10,8
user_type = 'routine_transactions'
pre_auction=simulation_action(sell_num,buy_num,user_type)          
buyer,seller=pre_auction.hh()   
seller.columns=['userid','price','quantity']
buyer.columns=['userid','price','quantity']
p=set_auction(seller,buyer)
buy_data,sell_data=p.pre_data()
df=p.compute()
assign_buy_quantity_result,assign_sell_quantity_result=p.assign_quantity()
buy_mean_voidance_result,sell_mean_voidance_result=p.mean_voidance()
e=p.unified_voidance()
d=p.undeal()
p.get_picture()
