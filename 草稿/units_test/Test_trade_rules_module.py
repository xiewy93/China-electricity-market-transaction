# -*- coding: utf-8 -*-
"""
Created on Wed May 10 15:11:51 2017

@author: lenovo
"""
import pandas as pd
import unittest
import trade_rules

class Test_trade_rules_module(unittest.TestCase):
    
    input_sell = pd.DataFrame(
                [['sell_3',-0.26,400],
                ['sell_2',-0.25,300]])
    
    output_sell = pd.DataFrame(
                [['sell_3',-0.26,400],
                ['sell_2',-0.25,300]])
    
    input_buy = pd.DataFrame(
               [['buy_3',-0.26, 300],
               ['buy_2',-0.25, 400]])
    
    output_buy = pd.DataFrame(
                [['buy_2',-0.25, 400],
                ['buy_3',-0.26, 300]])
    
    compute_sum_deal_quantity = pd.DataFrame(
                               [[-0.25,-0.26, 400],
                               [-0.26,-0.25, 300]])
    
    mean_voidance = pd.Series([[-0.255], [-0.255]])
    
    unified_voidance = pd.Series([[-0.255], [-0.255]])
    
    return_undeal = pd.Series([0, 0])
    #初始化工作  
    def setUp(self):  
        self.tclass = trade_rules.trade_rules()  
    
    #退出清理工作  
    def tearDown(self):  
        pass  

    #具体的测试用例，一定要以test开头 
    
    def test_init_participants(self):  
        self.assertEqual(self.tclass.init_participants(self.input_sell, True), self.output_sell)  
        
        
    def test_compute_sum_deal_quantity(self):
        self.assertEqual(self.tclass.compute_sum_deal_quantity(),self.compute_sum_deal_quantity)                
        
    def test_mean_voidance(self):
        self.assertEqual(self.tclass.mean_voidance(),self.mean_voidance)
        
    def test_unified_voidance(self):
        self.assertEqual(self.tclass.unified_voidance(),self.unified_voidance)
        
    def test_return_undeal(self):
        self.assertEqual(self.tclass.return_undeal(),self.return_undeal)

        
if __name__ =='__main__':  
    unittest.main()