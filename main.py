#!/usr/bin/env Python2.7
# coding=UTF-8
import os
import re
import utility
import psycopg2
import datetime
import json


def column_dealer(querycolumn):
    result = ''
    a = querycolumn.strip().split(' ')
    c_name = a[0]
    c_type = a[1]
    c_allow_null = True
    # created_at timestamp without time zone,
    if len(a) > 3:
        for i in range(len(a) - 1):
            if a[i].upper() == 'NOT' and a[i + 1].upper() == 'NULL':
                c_allow_null = False
    a_name = alphabet_dealer(c_name)
    # Get go type from column type
    go_data_type = ''
    if c_type in [
        'serial', 'serial4', 'smallserial', 'serial2', 'integer',
        'int', 'int4', 'smallint', 'int2'
    ]:
        go_data_type = 'int'
    elif c_type in ['bigserial', 'serial8', 'bigint', 'int8']:
        go_data_type = 'int64'
    elif c_type in ['text']:
        go_data_type = 'string'
    elif c_type in ['timestamp']:
        go_data_type = 'time.Time'
    elif c_type in ['bool']:
        go_data_type = 'bool'
    elif c_type in ['real', 'float4']:
        go_data_type = 'float32'
    elif c_type in ['float8']:
        go_data_type = 'float64'
    if c_allow_null is True and c_name != 'id':
        go_data_type = '*' + go_data_type
    if re.search('[^a-z]*id[^a-z]*', c_name) is not None:
        a_name = a_name.replace('Id', 'ID')
    item = utility.JsonItemClass()
    item.column_name = c_name
    item.attribute_name = a_name
    item.parameter_name = a_name[0].lower() + a_name[1:]
    item.go_data_type = go_data_type
    return item


def alphabet_dealer(c_name):
    a = c_name.split('_')
    result = ''
    for v in a:
        if v == 'id':
            result += v.upper()
        elif v == 'ids':
            result += 'IDs'
        elif v == 'url':
            result += 'URL'
        else:
            result += v[0].upper() + v[1:]
    return result


def model_str(items):
    return '\n'.join(['{0}\t{1}\t`json:"{2}"`'.format(
        v.attribute_name, v.go_data_type, v.column_name) for v in items]) + '\n'


def selectx_rowscan_str(items):
    return ', '.join(['&item.{0}'.format(v.attribute_name) for v in items])


def insert_query_str(items):
    part1 = '\t\t' + ',\n\t\t'.join([v.column_name for v in items
                                     if v.attribute_name != 'ID'])
    part2 = ', '.join(['${0}'.format(k) for k, v in enumerate(items)
                       if v.attribute_name != 'ID'])
    return '(\n{0})\n\tVALUES ({1})'.format(part1, part2)


def insert_queryrow_str(items):
    return ', '.join(['item.{0}'.format(v.attribute_name) for v in items
                      if v.attribute_name != 'ID'])


def update_query_str(items):
    return ',\n\t\t'.join(['{0} = ${1}'.format(v.column_name, k + 1)
                           for k, v in enumerate(items)
                           if v.attribute_name != 'ID'])


def wrapper_str(items):
    return '\n'.join(['newitem.{0} = item.{0}'.format(v.attribute_name)
                      for v in items])


def sortby_comparedfunc_str(items):
    return ' else '.join(["""if columnName == "{0}" {{
        return typeCompareFunc(p1.{1}, p2.{1}, orderstr)
    }}""".format(v.column_name, v.attribute_name) for v in items
        if v.attribute_name != 'ID'])


def sortby_comparedfunc_str_default(items, i):
    return "return typeCompareFunc(p1.{1}, p2.{1}, orderstr)".format(
        items[i].column_name, items[i].attribute_name)


# don't support 'in' and '()' as a function parameter
def complex_where_str(column_dic, where_str):
    quiterias = re.findall(r'([a-z|\_]+\s*(?:\!\=|\=|\<\>)\s*\S+)', where_str)
    fix_quiterias = []
    dynamic_quiterias = []
    for v in quiterias:
        if re.search(r'%v', v) is not None:
            dynamic_quiterias.append(v)
        else:
            fix_quiterias.append(v)
    dynamic_quiterias_c_name_list = []

    for v in dynamic_quiterias:
        c_name = re.search(r'([a-z|\_]+)\s*(?:\!\=|\=|\<\>)\s*\S+', v).group(1)
        dynamic_quiterias_c_name_list.append(c_name)

    quiterias_connect = "and"
    if re.search(r'\s+(or)\s+', where_str) is not None:
        quiterias_connect = "or"

    func_para_str = ', '.join([column_dic[v].parameter_name + ' *' +
                               column_dic[v].go_data_type.replace('*', '')
                               for v in dynamic_quiterias_c_name_list])
    func_query_para_str = """quiteriaArray := []string{}\n"""
    func_query_para_str += '\n'.join(["""\tquiteriaArray = append(quiteriaArray, "{0}")""".format(v)
                                      for v in fix_quiterias])
    func_query_para_str += ''.join("""
        if {1} != nil {{
		quiteriaArray = append(quiteriaArray, fmt.Sprintf("{0} = %v", {1}))
	}}""".format(column_dic[v].column_name, column_dic[v].parameter_name)
        for v in dynamic_quiterias_c_name_list)
    func_query_para_str += """
        if len(quiteriaArray) != 0 {{
		querystr = querystr + " WHERE " + strings.Join(quiteriaArray, " {0} ")
	}}""".format(quiterias_connect)
    return func_para_str, func_query_para_str


def func_template_work(tpltfunctext, column_dic):
    tpltfunctext = tpltfunctext.replace('[func_name_str]', function_name)
    tpltfunctext = tpltfunctext.replace('[func_query_str]', function_query)
    # Have complex where or not
    has_complex_where = False
    where_str = re.search(r'\s+where((.|\n)*)', function_query)
    if where_str is not None:
        complex_where = re.search(r'%v', function_query)
        if complex_where is not None:
            has_complex_where = True
    if has_complex_where:
        func_para_str, func_query_para_str = complex_where_str(
            column_dic, where_str.group(1))
        tpltfunctext = tpltfunctext.replace('[func_para_str]', func_para_str)
        tpltfunctext = tpltfunctext.replace(
            '[func_query_para_str]', func_query_para_str)
    else:
        tpltfunctext = tpltfunctext.replace('[func_para_str]', '')
        tpltfunctext = tpltfunctext.replace(
            '[func_query_para_str]\n', '')
        if re.search(r'[tx_comma]', tpltfunctext) is not None:
            tpltfunctext = tpltfunctext.replace('[tx_comma]', '')
    # Return
    if function_return == 'struct':
        tpltfunctext = tpltfunctext.replace(
            '[func_return_para_str]', "*TableCreateDemo")
        tpltfunctext = tpltfunctext.replace(
            '[func_return_str]', """
        // Return single part code
        if insArr == nil || len(insArr) == 0 {
        	err = errors.New("cannot found the data row")
        	logger.StackLogger(err)
        	return nil, err
        }
        if len(insArr) > 1 {
        	err = errors.New("more than one data row in the search quiteria")
        	logger.StackLogger(err)
        	return nil, err
        }
        return insArr[0], err""")
    else:
        tpltfunctext = tpltfunctext.replace(
            '[func_return_para_str]', "[]*TableCreateDemo")
        tpltfunctext = tpltfunctext.replace(
            '[func_return_str]', """return insArr, err""")
    return tpltfunctext

# Read description
alltxt = open("db_description.txt").read().decode("utf-8").lower()

# For Create Table: Get information
tablecreatetxt = re.search(
    r'\[create\s{1}start\]((.|\n)*)\[create\s{1}end\]', alltxt).group(1)
tablename = re.search(
    r'create\s+table\s+([a-z|\_]+)\s+\(', tablecreatetxt).group(1)
modelname = alphabet_dealer(tablename)
instancename = modelname[0].lower() + modelname[1:]  # first character lower
columnbody = re.search(
    r'create\s+table\s+[a-z|\_]+\s+\(((.|\n)*)\)', tablecreatetxt).group(1)
column_items = [column_dealer(v) for v in columnbody.split(',')]
# For Create Table: Apply template
tpltext = open("template.go.txt").read()
tpltext = tpltext.replace("table_create_demo", tablename)
tpltext = tpltext.replace("TableCreateDemo", modelname)
tpltext = tpltext.replace("tableCreateDemo", instancename)
tpltext = tpltext.replace("[model_str]", model_str(column_items))
tpltext = tpltext.replace("[selectx_rowscan_str]",
                          selectx_rowscan_str(column_items))
tpltext = tpltext.replace("[insert_query_str]", insert_query_str(column_items))
tpltext = tpltext.replace("[insert_queryrow_str]",
                          insert_queryrow_str(column_items))
tpltext = tpltext.replace("[update_query_str]", update_query_str(column_items))
tpltext = tpltext.replace("[wrapper_str]", wrapper_str(column_items))
tpltext = tpltext.replace("[sortby_comparedfunc_str]",
                          sortby_comparedfunc_str(column_items))
open('result.go', 'w').write(tpltext)

# For Function Template
column_dic = {v.column_name: v for v in column_items}
functionalltxt = re.search(
    r'\[function\s{1}start\]\s*((.|\n)*)\s*\[function\s{1}end\]', alltxt).group(1)
functiontxt_list = []
for func_json_dic in json.loads(functionalltxt, "utf-8"):
    function_name = alphabet_dealer(func_json_dic['name'])
    function_query = func_json_dic['query']
    function_return = func_json_dic['return']
    select_para_str = re.search(
        r'select\s+((.|\n)*)\s+from', function_query).group(1)
    tpltfunctext = ""
    if select_para_str.strip() == '*':
        tpltfunctext = open('template_func.go.txt').read()
        tpltfunctext = func_template_work(tpltfunctext, column_dic)
    else:
        tpltfunctext = open('template_partial_func.go.txt').read()
        tpltfunctext = func_template_work(tpltfunctext, column_dic)
        column_name_list = [v.strip() for v in select_para_str.split(',')]
        selectx_rowscan_str = ', '.join(['&item.' + column_dic[v].attribute_name
                                         for v in column_name_list if v in column_dic])
        tpltfunctext = tpltfunctext.replace(
            '[selectx_rowscan_str]', selectx_rowscan_str)
    tpltfunctext = u"//{0} is a auto generated function from SQL query {1}\n".format(
        function_name, function_query) + tpltfunctext
    functiontxt_list.append(tpltfunctext.encode("utf-8"))
open('result.go', 'a').write('\n'.join(functiontxt_list))

# For New Struct Function Start
tpltnstrtext = open("template_new_struct.go.txt").read()
newstructfunctionalltxt = re.search(
    r'\[new\s{1}struct\s{1}function\s{1}start\]\s*((.|\n)*)\s*\[new\s{1}struct\s{1}function\s{1}end\]', alltxt).group(1)
for news_func_json_dic in json.loads(newstructfunctionalltxt, "utf-8"):
    function_name = alphabet_dealer(news_func_json_dic['function_name'])
    struct_name = alphabet_dealer(news_func_json_dic['struct_name'])
    function_query = news_func_json_dic['query']
    data_type_dic = {}
    for v in news_func_json_dic['data_type'].split(';'):
        dtti = v.split(':')
        data_type_dic[dtti[0].strip()] = dtti[1].strip()
    column_str = re.search(r'select\s+((.|\n)*)\s+from',
                           function_query).group(1)
    nst_column_items = []
    for v in column_str.split(','):
        item = utility.JsonItemClass()
        cs = v.split(' as ')
        if len(cs) == 2:
            item.column_name = cs[1].strip()
        elif len(cs) == 1:
            item.column_name = cs[0].strip()
        else:
            print "error"
        item.attribute_name = alphabet_dealer(item.column_name)
        item.go_data_type = data_type_dic[item.column_name]
        nst_column_items.append(item)
tpltnstrtext = tpltnstrtext.replace("TableCreateDemo", modelname)
tpltnstrtext = tpltnstrtext.replace("[query]", function_query)
tpltnstrtext = tpltnstrtext.replace("[function_name]", function_name)
tpltnstrtext = tpltnstrtext.replace("NewStructMethodModel", struct_name)
tpltnstrtext = tpltnstrtext.replace("newStructMethodModel", struct_name[
    0].lower() + struct_name[1:])
tpltnstrtext = tpltnstrtext.replace("[model_str]", model_str(nst_column_items))
tpltnstrtext = tpltnstrtext.replace("[selectx_rowscan_str]", ','.join(
    ['&item.{0}'.format(v.attribute_name) for v in nst_column_items]))
tpltnstrtext = tpltnstrtext.replace("[sortby_comparedfunc_str]",
                                    sortby_comparedfunc_str(nst_column_items))
tpltnstrtext = tpltnstrtext.replace("[sortby_comparedfunc_str_default]",
                                    sortby_comparedfunc_str_default(nst_column_items, 0))
open('result.go', 'a').write(tpltnstrtext)
# TODO: sorting method of new structure


# Create table
conn = psycopg2.connect(database="postgres", user="ciao", password="Kir0#alpha",
                        host="localhost", port="5433")
cur = conn.cursor()
cur.execute(tablecreatetxt)
conn.commit()
cur.execute("""
CREATE TABLE table_create_demo_two (
  id SERIAL PRIMARY KEY,
  int_demo int NOT NULL,
  text_demo text NOT NULL DEFAULT ''
);
""")
conn.commit()
nameList = ["赤羽信之介", "青木ひかり", "相沢雅", "藤井りな", "逢沢莉奈"]
for k, v in enumerate(nameList):
    cur.execute("""
        INSERT INTO table_create_demo(
        int_demo,
        text_demo,
        bool_demo,
        float_demo,
        timestamp_demo
        ) VALUES (%s,%s,%s,%s,%s)
        """, (k, v, False, 10.1, datetime.datetime.now()))
    conn.commit()
for k, v in enumerate(nameList):
    cur.execute("""
        INSERT INTO table_create_demo_two(
        int_demo,
        text_demo
        ) VALUES (%s,%s)
        """, (k, "<h3>{0}</h3>".format(v)))
    conn.commit()
cur.close()
conn.close()


# c_names = re.findall(
#    r'\s*[\(|\,]{1}\s*([a-z|\_]+)\s+[' + '|'.join(a) + ']+', tablecreatetxt)
# print c_names
