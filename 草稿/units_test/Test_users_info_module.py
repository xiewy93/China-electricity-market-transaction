# -*- coding: utf-8 -*-
"""
Created on Wed May 10 15:40:39 2017

@author: lenovo
"""

import unittest
import users_info
import simulation_action

class Test_simulation_action_module(unittest.TestCase):
    #初始化工作  
    def setUp(self):  
        self.tclass = users_info.users_info(simulation_action)  
    
    #退出清理工作  
    def tearDown(self):  
        pass  

    #具体的测试用例，一定要以test开头  
    def test_set_quantity(self):  
        self.assertEqual(self.tclass.set_quantity(3).nrows(), 3)  
   
    def test_set_assigned_price(self):  
        self.assertEqual(self.tclass.set_assigned_price(3).nrows(), 3) 

        
if __name__ =='__main__':  
    unittest.main()