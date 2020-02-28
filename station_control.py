# -*- coding: utf-8 -*-

import pandas as pd
import xlwings as xw
import datetime as dt

strategy_address = {'buy_strategy1':'a8',
                    'buy_strategy2':'a25',
                    'buy_strategy3':'a42',
                    'buy_strategy4':'a59',
                    'buy_strategy5':'a76',
                    'buy_strategy6':'a93',
                    'sell_strategy1':'a110',
                    'sell_strategy2':'a122',
                    'sell_strategy3':'a134'}

def sort_data(data):
    sort_result = data.sort_index()
    return sort_result


def set_rule_to_excel(rule_json):
    data = pd.read_json(rule_json)
    if data.empty:
        result = {'result':False,
                  'msg':'线上没有策略部署，请按照demo配置策略上传'}
        return result
    wb = xw.Book('huobi.xlsx')
    sht = wb.sheets('交易策略')
    for strategy,rng in strategy_address.items():
        piece_data = data[data.strategy == strategy]
        rule_list = [] 
        for rule in piece_data.rule_data:
            rule_list.append(eval(rule))
        rule_data = pd.DataFrame(rule_list).set_index('combin_id')
        table = sht.range(rng).expand('table')
        table.clear_contents()
        table.value = rule_data
    sht.activate()
    result = {'result':True,
              'msg':'规则已同步到EXCEL中'}
    return result

def get_rule_from_excel():
    wb = xw.Book('huobi.xlsx')
    sht = wb.sheets('交易策略')
    rule_data_list = []
    create_time = dt.datetime.now()
    for strategy,address in strategy_address.items():
        table = sht.range(address).expand('table')
        rule_data = table.options(pd.DataFrame).value.reset_index()
        for index in rule_data.index:
            rule_piece = rule_data.loc[index,:]        
            combin_id = int(rule_piece.loc['combin_id'])
            rule_json = str(rule_piece.to_dict())
            rule = pd.DataFrame([[strategy,rule_json,combin_id,str(create_time)]],
                                columns = ['strategy','rule_data','combin_id','create_time'])
            rule_data_list.append(rule)
    all_rule = pd.concat(rule_data_list).reset_index().iloc[:,1:]
    all_rule_json = all_rule.to_json()
    return all_rule_json

# 将线上使用的交易对放到excel中
def set_combin_strategy_to_excel(combin_strategy_json):
    data = pd.read_json(combin_strategy_json)
    if data.empty:
        result = {'result':False,
                  'msg':'当前线上没有使用的策略对，请配置策略并上传'}
        return result
    wb = xw.Book('huobi.xlsx')
    sht = wb.sheets('线上使用规则对')
    table = sht.range('c20').expand('table')
    table.clear_contents()
    sht.range('c20').value = data
    sht.activate()
    result = {'result':True,
              'msg':'策略已同步到execl中'}
    return result

# 获取mysql已经配置好的线上交易对
def get_combin_strategy_from_excel():
    wb = xw.Book('huobi.xlsx')
    sht = wb.sheets('线上使用规则对')
    table = sht.range('c20').expand('table')
    combin_strategy = table.options(pd.DataFrame).value
    combin_strategy.index = range(len(combin_strategy))
    combin_strategy_json = combin_strategy.to_json()
    return combin_strategy_json

#在售订单放入到excel中
def set_selling_orders(selling_orders_json):
    data = pd.read_json(selling_orders_json).set_index('symbol')
    wb = xw.Book('huobi.xlsx')
    sht = wb.sheets('在售订单')
    table = sht.range('a1').expand('table')
    table.clear_contents()
    table.value = data
    sht.activate()
    result = {'result':True,
              'msg':'在售订单已同步到excel中'}
    return result

#完结订单放入到excel中
def set_over_orders(over_orders_json):
    data = pd.read_json(over_orders_json).set_index('symbol')
    wb = xw.Book('huobi.xlsx')
    sht = wb.sheets('完结订单')
    table = sht.range('a1').expand('table')
    table.clear_contents()
    table.value = data
    sht.activate()
    result = {'result':True,
              'msg':'完结订单已同步到excel中'}
    return result    

#将symbollist输出到excel中
def set_symbol_list(symbol_list_json):
    data = pd.read_json(symbol_list_json)
    wb = xw.Book('huobi.xlsx')
    sht = wb.sheets('交易对')
    table = sht.range('a1').expand('table').options(index = False)
    table.clear_contents()
    table.value = data
    sht.activate()
    result = {'result':True,
              'msg':'交易对已同步到excel中'}
    return result    

def get_symbol_list():
    wb = xw.Book('huobi.xlsx')
    sht = wb.sheets('交易对')
    table = sht.range('a1').expand('table')
    symbol_data = table.options(pd.DataFrame,index = False).value
    symbol_list_json = symbol_data.to_json()
    return symbol_list_json
    
    
