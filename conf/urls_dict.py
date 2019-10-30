# -*- coding: utf-8 -*-


localhost = 'http://127.0.0.1:8000'
host = 'http://47.52.39.163:8000'
#use_host = localhost
use_host = host

urls_dict = {
            'login':'%s/hb/login'%use_host,
            'zhuce':'%s/hb/zhuce'%use_host,
            'upload_key':'%s/hb/upload_key'%use_host,
            'update_reg_key':'%s/hb/update_reg_key'%use_host,
            'get_rule':'%s/hb/get_rule'%use_host,
            'send_rule':'%s/hb/send_rule'%use_host,
            'get_combin_strategy':'%s/hb/get_combin_strategy'%use_host,
            'send_combin_strategy':'%s/hb/send_combin_strategy'%use_host,
            'get_selling_orders':'%s/hb/get_selling_orders'%use_host,
            'get_over_orders':'%s/hb/get_over_orders'%use_host,
            'get_symbol_list':'%s/hb/get_symbol_list'%use_host,
            'update_symbol_list':'%s/hb/update_symbol_list'%use_host,
            'sellordersbyself':'%s/hb/sellordersbyself'%use_host,
             }

