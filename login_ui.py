# -*- coding: utf-8 -*-

import tkinter as tk
import urllib
import json

from conf.urls_dict import urls_dict
from station_control import (set_rule_to_excel,
                            get_rule_from_excel,
                            set_combin_strategy_to_excel,
                            get_combin_strategy_from_excel,
                            set_selling_orders,
                            set_over_orders,
                            set_symbol_list,
                            get_symbol_list)


def get_response(url,data):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
    data = urllib.parse.urlencode(data).encode()
    
    req = urllib.request.Request(url,data = data,headers = headers)
    
    response = urllib.request.urlopen(req,timeout = 30).read()
    result = response.decode()
    return result

#登录/注册界面
class LoginUi(object):
    def __init__(self):
        self.root = tk.Tk()        
#        self.root = tk.Toplevel()
        self.root.title('登陆/注册')
        self.root.geometry("350x200")
        self.frm = tk.Frame(self.root)
        tk.Label(self.frm,text = '      状态:      ').grid(row=1,column=1,pady=10)
        self.text = tk.Text(self.frm,font=("微软雅黑",10),width = 30,height = 3)
        self.text.grid(row=1,column = 2)
        
        value_text_list = ['账号:','密码:']
        self.var_dict = {}
        row = 2
        for value_key in value_text_list:
            tk.Label(self.frm,text = value_key).grid(row=row,column=1,pady=10)
            self.var_dict[value_key]= tk.Variable()
            self.text1 = tk.Entry(self.frm,
                                  font=("微软雅黑",10),
                                  width = 30,
                                  textvariable=self.var_dict[value_key]).grid(row=row,column = 2)
            row = row + 1
            
        button_dict = {'登陆':self.login,
                       '注册':self.zhuce}
        
        self.frm2 = tk.Frame(self.root)
        col = 1
        for button in button_dict:
            tk.Button(self.frm2,
                      text = button,
                      font=("微软雅黑",10),
                      command = button_dict[button],
                      width =10,
                      height =1).grid(row = 1,column = col,padx = 30)
            col = col + 1
        self.frm.grid(row = 1)
        self.frm2.grid(row = 2)
        
        self.root.mainloop()
        
    def insert_text(self,msg):
        self.text.delete(0.1,2.0)
        self.text.insert(tk.INSERT,msg + '\n')
    #登陆完成
    def login(self):
        phone = self.var_dict['账号:'].get()
        password = self.var_dict['密码:'].get()
        url = urls_dict['login']
        data = {'phone':phone,
                'password':password}
        response = get_response(url,data)
        login_result = json.loads(response)
        self.insert_text(login_result['msg'])
        if login_result['result']:
            self.uid = int(login_result.get('uid',''))
            self.root.destroy()
            ControlUi(self.uid)
    
    def zhuce(self):
        self.root.destroy()
        ZhuCe()

#注册界面
class ZhuCe(object):
    def __init__(self):
        self.root = tk.Tk()        
        self.root.title('注册')
        self.root.geometry("350x400")
        self.frm = tk.Frame(self.root)
        tk.Label(self.frm,text = '      状态:      ').grid(row=1,column=1,pady=10)
        self.text = tk.Text(self.frm,font=("微软雅黑",10),width = 30,height = 3)
        self.text.grid(row=1,column = 2)
        
        self.value_text_list = ['姓名:',
                           '手机号:',
                           '身份证号:',
                           '密码:',
                           '请再次输入密码:',
                           '购买的校验码:'
                           ]
        self.var_dict = {}
        row = 2
        for value_key in self.value_text_list:
            tk.Label(self.frm,text = value_key).grid(row=row,column=1,pady=10)
            self.var_dict[value_key]= tk.Variable()
            self.text1 = tk.Entry(self.frm,
                                  font=("微软雅黑",10),
                                  width = 30,
                                  textvariable=self.var_dict[value_key]).grid(row=row,column = 2)
            row = row + 1
            
        button_dict = {'返回':self.click_back,
                       '注册':self.zhuce}
        self.frm2 = tk.Frame(self.root)
        col = 1
        for button in button_dict:
            tk.Button(self.frm2,
                      text = button,
                      font=("微软雅黑",10),
                      command = button_dict[button],
                      width =10,
                      height =1).grid(row = 1,column = col,padx = 30)
            col = col + 1
        self.frm.grid(row = 1)
        self.frm2.grid(row = 2)
        
        self.root.mainloop()
    
    def insert_text(self,msg):
        self.text.delete(0.1,2.0)
        self.text.insert(tk.INSERT,msg + '\n')
        
    def click_back(self):
        self.root.destroy()
        LoginUi()
    def zhuce(self):
        name = self.var_dict['姓名:'].get()
        phone = self.var_dict['手机号:'].get()
        idcard = self.var_dict['身份证号:'].get()
        password1 = self.var_dict['密码:'].get()
        password2 = self.var_dict['请再次输入密码:'].get()
        reg_key = self.var_dict['购买的校验码:'].get()
        url = urls_dict['zhuce']
        data = {'name':name,
                'phone':phone,
                'idcard':idcard,
                'password1':password1,
                'password2':password2,
                'reg_key':reg_key
                }
        
        create_result = get_response(url,data)
        create_result = json.loads(create_result)
        self.insert_text(create_result['msg'])

class ControlUi(object):
    def __init__(self,uid):
        self.uid = uid
        print(self.uid)
        self.root = tk.Tk()        
        self.root.title('操控台')
        self.root.geometry("500x500")
        self.frm = tk.Frame(self.root)
        tk.Label(self.frm,text = '      状态:      ').grid(row=1,column=1,pady=10)
        self.text = tk.Text(self.frm,font=("微软雅黑",10),width = 50,height = 3)
        self.text.grid(row=1,column = 2)
        
        self.value_text_list = ['access_key:',
                               'secret_key:',
                               '注册码:',
                               'symbol:'
                               ]
        self.var_dict = {}
        row = 2
        for value_key in self.value_text_list:
            tk.Label(self.frm,text = value_key).grid(row=row,column=1,pady=10)
            self.var_dict[value_key]= tk.Variable()
            self.text1 = tk.Entry(self.frm,
                                  font=("微软雅黑",10),
                                  width = 50,
                                  textvariable=self.var_dict[value_key]).grid(row=row,column = 2)
            row = row + 1
            
        button_dict = {'上传/更新key':self.save_key_to_table,
                       '更新注册码':self.update_key,
                       '配置规则':self.get_rule,
                       '保存规则':self.send_rule,
                       '制定策略':self.make_strategy,
                       '上线策略':self.send_strategy,
                       '查看在售订单':self.selling_orders,
                       '查看完结订单':self.seld_orders,
                       '查看交易对':self.select_symbol_list,
                       '更新交易对':self.update_symbol_list,
                       'sell_market':self.sell_orders_byself,
                       '返回登陆':self.back
                       }
        self.frm2 = tk.Frame(self.root)
        col = 1
        row1 = 1
        for button in button_dict:
            tk.Button(self.frm2,
                      text = button,
                      font=("微软雅黑",10),
                      command = button_dict[button],
                      width =10,
                      height =1).grid(row = row1,column = col,padx = 10,pady = 10)
            if col == 4:
                row1 = row1 + 1
                col = 0
            col = col + 1
        self.frm.grid(row = 1)
        self.frm2.grid(row = 2)
        
        self.frm.grid(row = 1)
        self.root.mainloop()
    
    
    def insert_text(self,msg):
        self.text.delete(0.1,2.0)
        self.text.insert(tk.INSERT,msg + '\n')
    # 上传KEY
    def save_key_to_table(self):
        url = urls_dict['upload_key']
        data = {'uid':self.uid,
                'access_key':self.var_dict['access_key:'].get(),
                'secret_key':self.var_dict['secret_key:'].get(),
                'reg_key':self.var_dict['注册码:'].get(),
                }
        print(data)
        response = get_response(url,data)
        result = json.loads(response)
        self.insert_text(result['msg'])
        
    # 更新注册码
    def update_key(self):
        url = urls_dict['update_reg_key']
        data = {'uid':self.uid,
                'reg_key':self.var_dict['注册码:'].get(),
                }
        print(data)
        response = get_response(url,data)
        result = json.loads(response)
        self.insert_text(result['msg'])
        
    # 获取线上规则  
    def get_rule(self):
        url = urls_dict['get_rule']
        data = {'uid':self.uid,
                }
        response  = get_response(url,data)
        result = set_rule_to_excel(response)
        self.insert_text(result['msg'])
    # 更新规则
    def send_rule(self):
        url = urls_dict['send_rule']
        rule_json = get_rule_from_excel()
        uid = self.uid
        data = {'uid':uid,
                'rule_json':rule_json}
        response = get_response(url,data)
        result = json.loads(response)
        self.insert_text(result['msg'])
        
    def make_strategy(self):
        url = urls_dict['get_combin_strategy']
        data = {'uid':self.uid,
                }
        response  = get_response(url,data)
        result = set_combin_strategy_to_excel(response)
        self.insert_text(result['msg'])

    def send_strategy(self):
        url = urls_dict['send_combin_strategy']
        combin_strategy_json = get_combin_strategy_from_excel()
        uid = self.uid
        data = {'uid':uid,
                'combin_strategy_json':combin_strategy_json}
        response = get_response(url,data)
        result = json.loads(response)
        self.insert_text(result['msg'])
    
    def selling_orders(self):
        url = urls_dict['get_selling_orders']
        data = {'uid':self.uid,
                }
        response  = get_response(url,data)
        result = set_selling_orders(response)
        self.insert_text(result['msg'])
    
    def seld_orders(self):
        url = urls_dict['get_over_orders']
        data = {'uid':self.uid,
                }
        response  = get_response(url,data)
        result = set_over_orders(response)
        self.insert_text(result['msg'])
    
    def select_symbol_list(self):
        url = urls_dict['get_symbol_list']
        data = {'uid':self.uid,
                }
        response  = get_response(url,data)
        result = set_symbol_list(response)
        self.insert_text(result['msg'])
    
    def update_symbol_list(self):
        url = urls_dict['update_symbol_list']
        symbol_list_json = get_symbol_list()
        uid = self.uid
        data = {'uid':uid,
                'symbol_list_json':symbol_list_json}
        response = get_response(url,data)
        result = json.loads(response)
        self.insert_text(result['msg'])
        
    def sell_orders_byself(self):
        url = urls_dict['sellordersbyself']
        uid = self.uid
        symbol = self.var_dict['symbol:'].get()
        data = {'uid':uid,
                'symbol':symbol.lower()}
        print(data)
        response = get_response(url,data)
        result = json.loads(response)
        self.insert_text(result['msg'])
        
    def back(self):
        self.root.destroy()
        LoginUi()
login_obj = LoginUi()
